import random
from collections import Counter
from datetime import date

import pytest

from skillzor.models import (
    Certification,
    Employee,
    EmployeeCertification,
    EmployeeSkill,
    Skill,
)
from skillzor.privacy import (
    SuppressionReport,
    _generalise_quasi_identifiers,
    build_export,
    pseudonymize,
)


class FakeEmployee:
    def __init__(self, id, department, job_title):
        self.id = id
        self.department = department
        self.job_title = job_title


def make_org(spec):
    """spec: list of (department, job_title, count)"""
    out, i = [], 0
    for dept, title, count in spec:
        for _ in range(count):
            i += 1
            out.append(FakeEmployee(i, dept, title))
    return out


def released_groups(mapping):
    return Counter(mapping.values())


# --- pseudonymisation -------------------------------------------------------


def test_pseudonym_is_stable_and_key_dependent():
    assert pseudonymize(1, b"a") == pseudonymize(1, b"a")  # nosec B101
    assert pseudonymize(1, b"a") != pseudonymize(2, b"a")  # nosec B101
    assert pseudonymize(1, b"a") != pseudonymize(1, b"b")  # nosec B101


def test_pseudonym_does_not_contain_id():
    p = pseudonymize(123456, b"key")
    assert "123456" not in p  # nosec B101
    assert len(p) == 20  # nosec B101


# --- generalisation ---------------------------------------------------------


def test_lone_title_is_folded_into_a_big_enough_bucket():
    # 6 devs + 1 architect: dropping only the architect's title would leave a
    # bucket of one, which is just as identifying as the title itself.
    org = make_org([("Eng", "Dev", 6), ("Eng", "Architect", 1)])
    mapping = _generalise_quasi_identifiers(org, 5, SuppressionReport(k=5))
    assert set(released_groups(mapping)) == {("Eng", None)}  # nosec B101


def test_common_titles_survive():
    org = make_org([("Eng", "Dev", 5), ("Eng", "QA", 5), ("Eng", "Arch", 5)])
    mapping = _generalise_quasi_identifiers(org, 5, SuppressionReport(k=5))
    assert released_groups(mapping) == {  # nosec B101
        ("Eng", "Dev"): 5,
        ("Eng", "QA"): 5,
        ("Eng", "Arch"): 5,
    }


def test_small_departments_are_suppressed_together():
    org = make_org([("Eng", "Dev", 5), ("Sales", "AM", 3), ("Legal", "LC", 2)])
    report = SuppressionReport(k=5)
    mapping = _generalise_quasi_identifiers(org, 5, report)
    assert released_groups(mapping) == {  # nosec B101
        ("Eng", "Dev"): 5,
        (None, None): 5,
    }
    assert report.departments_suppressed == 5  # nosec B101


def test_population_smaller_than_k_releases_nothing():
    org = make_org([("Eng", "Dev", 4)])
    assert (
        _generalise_quasi_identifiers(org, 5, SuppressionReport(k=5)) is None
    )  # nosec B101


@pytest.mark.parametrize("seed", range(300))
def test_every_released_bucket_has_at_least_k_members(seed):
    """Property test: the k-anonymity guarantee holds for random org charts."""
    rng = random.Random(seed)
    k = rng.randint(2, 8)
    spec = [
        (f"D{d}", f"T{t}", rng.randint(1, 9))
        for d in range(rng.randint(1, 6))
        for t in range(rng.randint(1, 5))
    ]
    org = make_org(spec)
    mapping = _generalise_quasi_identifiers(org, k, SuppressionReport(k=k))
    if len(org) < k:
        assert mapping is None  # nosec B101
        return
    assert len(mapping) == len(org)  # nosec B101  (nobody is silently dropped)
    assert min(released_groups(mapping).values()) >= k  # nosec B101


# --- full export ------------------------------------------------------------


@pytest.fixture
def org_with_rare_attributes(db):
    common = Skill.objects.create(
        name="Python", description="", framework_ref="e-CF:B.1"
    )
    rare = Skill.objects.create(name="COBOL", description="")
    cert = Certification.objects.create(name="ISTQB", issuer="ISTQB", description="")
    rare_cert = Certification.objects.create(
        name="CISSP", issuer="ISC2", description=""
    )
    employees = []
    for i in range(5):
        e = Employee.objects.create(
            first_name=f"First{i}",
            last_name=f"Last{i}",
            department="Eng",
            job_title="Dev",
        )
        EmployeeSkill.objects.create(employee=e, skill=common, proficiency_level=3)
        EmployeeCertification.objects.create(
            employee=e,
            certification=cert,
            issue_date=date(2024, 3, 14),
            evidence="Badge #42",
        )
        employees.append(e)
    EmployeeSkill.objects.create(employee=employees[0], skill=rare, proficiency_level=5)
    EmployeeCertification.objects.create(
        employee=employees[0], certification=rare_cert, issue_date=date(2023, 1, 1)
    )
    return employees


def test_export_contains_no_direct_identifiers(org_with_rare_attributes):
    export = build_export(k=5, key=b"test")
    blob = repr(export)
    for e in org_with_rare_attributes:
        assert e.first_name not in blob  # nosec B101
        assert e.last_name not in blob  # nosec B101
    assert "Badge #42" not in blob  # nosec B101  (free-text evidence)
    assert "2024-03-14" not in blob  # nosec B101  (exact dates)
    assert {
        c["issued_year"] for r in export["records"] for c in r["certifications"]
    } == {
        2024
    }  # nosec B101


def test_export_drops_rare_skills_and_certifications(org_with_rare_attributes):
    export = build_export(k=5, key=b"test")
    skill_ids = {s["skill_id"] for r in export["records"] for s in r["skills"]}
    cert_ids = {
        c["certification_id"] for r in export["records"] for c in r["certifications"]
    }
    assert skill_ids == {Skill.objects.get(name="Python").id}  # nosec B101
    assert cert_ids == {Certification.objects.get(name="ISTQB").id}  # nosec B101
    assert export["privacy"]["rare_skills_dropped"] == 1  # nosec B101
    assert export["privacy"]["rare_certifications_dropped"] == 1  # nosec B101


def test_export_withholds_everything_for_tiny_population(db):
    Employee.objects.create(
        first_name="A", last_name="B", department="X", job_title="Y"
    )
    export = build_export(k=5, key=b"test")
    assert export["records"] == []  # nosec B101
    assert export["privacy"]["withheld"] is True  # nosec B101


def test_k_must_be_positive():
    with pytest.raises(ValueError):
        build_export(k=0)
