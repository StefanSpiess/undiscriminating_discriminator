"""
Privacy-preserving export of skill profiles for downstream AI/analytics systems.

The export implements the "blind data" principle from the design notes in
``background/``: models downstream should learn from skills and achievements,
never from names or other direct identifiers.

Guarantees (and their limits) are documented in ``docs/ai_export.md``:

* **Pseudonymisation** – employees are referenced by a keyed HMAC of their
  internal ID. Without ``PSEUDONYM_KEY`` the pseudonym cannot be linked back.
  Rotating the key unlinks all previous exports.
* **Data minimisation** – names, free-text evidence and exact dates are never
  exported. Certification dates are coarsened to the year.
* **k-anonymity on quasi-identifiers** – ``department`` and ``job_title`` are
  generalised step by step until every combination is shared by at least
  ``k`` employees; anything still too rare is suppressed.
* **Rare attribute suppression** – skills and certifications held by fewer
  than ``k`` employees are dropped, because a rare skill can single out a
  person as reliably as a name.
"""

from __future__ import annotations

import hashlib
import hmac
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from django.conf import settings
from django.utils.timezone import now

from .models import Employee, EmployeeCertification, EmployeeSkill

SUPPRESSED = None


def pseudonymize(employee_id: int, key: bytes | None = None) -> str:
    """Return a stable, non-reversible pseudonym for an employee ID."""
    key = key if key is not None else settings.PSEUDONYM_KEY.encode()
    digest = hmac.new(key, f"employee:{employee_id}".encode(), hashlib.sha256)
    return digest.hexdigest()[:20]


@dataclass
class SuppressionReport:
    k: int
    employees: int = 0
    job_titles_generalised: int = 0
    departments_suppressed: int = 0
    rare_skills_dropped: list[int] = field(default_factory=list)
    rare_certifications_dropped: list[int] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "k": self.k,
            "employees": self.employees,
            "job_titles_generalised": self.job_titles_generalised,
            "departments_suppressed": self.departments_suppressed,
            "rare_skills_dropped": len(self.rare_skills_dropped),
            "rare_certifications_dropped": len(self.rare_certifications_dropped),
            "withheld": False,
        }


def _fold_small_buckets(groups: dict, residual: list, k: int) -> list:
    """
    Move the smallest groups into ``residual`` until the residual bucket is
    either empty or holds at least k members. Mutates ``groups``.
    """
    while 0 < len(residual) < k and groups:
        smallest = min(groups, key=lambda g: (len(groups[g]), str(g)))
        residual.extend(groups.pop(smallest))
    return residual


def _generalise_quasi_identifiers(employees, k: int, report: SuppressionReport):
    """
    Map employee id -> (department, job_title) such that every released
    combination, including the generalised ones, is shared by >= k employees.

    1. Within each department, job titles shared by < k people are replaced by
       ``None``. If that "(dept, None)" bucket is itself smaller than k, the
       smallest intact title groups are folded into it until it is big enough.
    2. Departments with < k members are suppressed entirely. The resulting
       "(None, None)" bucket is grown the same way, by folding in the smallest
       remaining departments.
    3. If the whole population is smaller than k, nothing can be released.
    """
    if len(employees) < k:
        return None

    by_dept = defaultdict(list)
    for e in employees:
        by_dept[e.department].append(e)

    # Step 2 first: decide which departments survive at all.
    small_depts = [d for d, members in by_dept.items() if len(members) < k]
    suppressed = [e for d in small_depts for e in by_dept.pop(d)]
    _fold_small_buckets(by_dept, suppressed, k)

    result = {e.id: (SUPPRESSED, SUPPRESSED) for e in suppressed}
    report.departments_suppressed = len(suppressed)

    # Step 1: titles within surviving departments.
    for dept, members in by_dept.items():
        by_title = defaultdict(list)
        for e in members:
            by_title[e.job_title].append(e)
        rare_titles = [t for t, grp in by_title.items() if len(grp) < k]
        generalised = [e for t in rare_titles for e in by_title.pop(t)]
        _fold_small_buckets(by_title, generalised, k)

        for e in generalised:
            result[e.id] = (dept, SUPPRESSED)
        report.job_titles_generalised += len(generalised)
        for title, grp in by_title.items():
            for e in grp:
                result[e.id] = (dept, title)
    return result


def build_export(k: int, key: bytes | None = None) -> dict:
    """Build the pseudonymised, k-anonymised export payload."""
    if k < 1:
        raise ValueError("k must be >= 1")

    employees = list(Employee.objects.only("id", "department", "job_title"))
    report = SuppressionReport(k=k, employees=len(employees))
    quasi = _generalise_quasi_identifiers(employees, k, report)
    if quasi is None:
        # Population too small to release anything safely.
        return {
            "generated_at": now().isoformat(),
            "schema_version": 1,
            "privacy": {**report.as_dict(), "withheld": True},
            "records": [],
        }

    skills = list(
        EmployeeSkill.objects.select_related("skill").only(
            "employee_id", "proficiency_level", "skill__id", "skill__framework_ref"
        )
    )
    certs = list(
        EmployeeCertification.objects.only(
            "employee_id", "certification_id", "issue_date"
        )
    )

    skill_holders = Counter(s.skill_id for s in skills)
    cert_holders = Counter(c.certification_id for c in certs)
    report.rare_skills_dropped = sorted(
        sid for sid, n in skill_holders.items() if n < k
    )
    report.rare_certifications_dropped = sorted(
        cid for cid, n in cert_holders.items() if n < k
    )
    rare_skills = set(report.rare_skills_dropped)
    rare_certs = set(report.rare_certifications_dropped)

    skills_by_emp = defaultdict(list)
    for s in skills:
        if s.skill_id in rare_skills:
            continue
        skills_by_emp[s.employee_id].append(
            {
                "skill_id": s.skill_id,
                "framework_ref": s.skill.framework_ref or None,
                "level": s.proficiency_level,
            }
        )

    certs_by_emp = defaultdict(list)
    for c in certs:
        if c.certification_id in rare_certs:
            continue
        certs_by_emp[c.employee_id].append(
            {"certification_id": c.certification_id, "issued_year": c.issue_date.year}
        )

    records = []
    for e in employees:
        department, job_title = quasi[e.id]
        records.append(
            {
                "pseudonym": pseudonymize(e.id, key),
                "department": department,
                "job_title": job_title,
                "skills": sorted(skills_by_emp[e.id], key=lambda x: x["skill_id"]),
                "certifications": sorted(
                    certs_by_emp[e.id], key=lambda x: x["certification_id"]
                ),
            }
        )
    # Order by pseudonym so the output order does not leak database IDs.
    records.sort(key=lambda r: r["pseudonym"])

    return {
        "generated_at": now().isoformat(),
        "schema_version": 1,
        "privacy": report.as_dict(),
        "records": records,
    }
