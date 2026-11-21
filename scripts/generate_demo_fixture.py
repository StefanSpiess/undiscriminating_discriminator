"""
Generate ``undiscriminate/fixtures/demo_org.json``: a fictional company that
exercises every branch of the k-anonymity logic at the default k=5.

* Engineering: large, mostly common job titles plus one lone architect
  (title gets generalised).
* Data: one common title plus a rare one (folding of small title groups).
* People & Culture: exactly k members (department survives, title kept).
* Sales / Legal: each smaller than k, together exactly k (suppressed jointly).
* One skill and one certification held by a single person (rare attributes).

All names are invented. Run: ``python scripts/generate_demo_fixture.py``
"""

import json
import random
from datetime import date
from pathlib import Path

# Deterministic demo data; not used for anything security relevant.
rng = random.Random(42)  # nosec B311

FIRST = [
    "Alex",
    "Sam",
    "Robin",
    "Kim",
    "Jona",
    "Mika",
    "Luca",
    "Noa",
    "Kai",
    "Lio",
    "Toni",
    "Charlie",
    "Sascha",
    "Nikola",
    "Maxi",
    "Ari",
    "Jule",
    "Remi",
    "Elia",
    "Fenja",
    "Ole",
    "Pia",
    "Quinn",
    "Rune",
    "Sila",
    "Tjark",
    "Uma",
    "Vida",
    "Wim",
    "Yara",
]
LAST = [
    "Amsel",
    "Birke",
    "Clausen",
    "Dorn",
    "Eiche",
    "Falk",
    "Gerste",
    "Hafer",
    "Iltis",
    "Jansen",
    "Kranich",
    "Linde",
    "Moor",
    "Nessel",
    "Otter",
    "Pappel",
    "Quendel",
    "Rabe",
    "Specht",
    "Tanne",
    "Ulme",
    "Vogt",
    "Weide",
    "Ysop",
    "Zeder",
    "Adler",
    "Buche",
    "Dachs",
    "Erle",
    "Fichte",
]

# (department, job_title, headcount)
ORG = [
    ("Engineering", "Software Engineer", 9),
    ("Engineering", "QA Engineer", 5),
    ("Engineering", "Solution Architect", 1),
    ("Data", "Data Scientist", 6),
    ("Data", "Data Engineer", 2),
    ("People & Culture", "HR Business Partner", 5),
    ("Sales", "Account Manager", 3),
    ("Legal", "Legal Counsel", 2),
]

# e-CF 4.0 competences (code, name, description)
SKILLS = [
    (
        "A.5",
        "Architecture Design",
        "Specifies and refines the overall ICT architecture.",
    ),
    ("A.6", "Application Design", "Designs ICT solutions that meet business needs."),
    ("B.1", "Application Development", "Builds and maintains software applications."),
    ("B.3", "Testing", "Designs and executes test plans and quality checks."),
    (
        "D.7",
        "Data Science and Analytics",
        "Derives insights from data with statistical methods.",
    ),
    (
        "D.10",
        "Information and Knowledge Management",
        "Structures and shares organisational knowledge.",
    ),
    (
        "D.11",
        "Needs Identification",
        "Clarifies customer requirements and translates them into solutions.",
    ),
    (
        "E.2",
        "Project and Portfolio Management",
        "Plans and steers projects to agreed outcomes.",
    ),
    (
        "E.8",
        "Information Security Management",
        "Implements and maintains security controls.",
    ),
]

SKILLS_BY_TITLE = {
    "Software Engineer": ["A.6", "B.1", "B.3"],
    "QA Engineer": ["B.3", "B.1"],
    "Solution Architect": ["A.5", "A.6", "E.8"],
    "Data Scientist": ["D.7", "D.10", "B.1"],
    "Data Engineer": ["B.1", "D.7"],
    "HR Business Partner": ["D.10", "D.11", "E.2"],
    "Account Manager": ["D.11", "E.2"],
    "Legal Counsel": ["D.10"],
}

CERTS = [
    (
        "ISTQB Certified Tester Foundation Level",
        "ISTQB",
        ["QA Engineer", "Software Engineer"],
    ),
    (
        "Professional Scrum Master I",
        "Scrum.org",
        ["Software Engineer", "HR Business Partner"],
    ),
    (
        "Certified Information Systems Security Professional",
        "ISC2",
        ["Solution Architect"],
    ),
]


def main():
    out = []
    for i, (code, name, desc) in enumerate(SKILLS, start=1):
        out.append(
            {
                "model": "skillzor.skill",
                "pk": i,
                "fields": {
                    "name": name,
                    "description": desc,
                    "category": "e-CF 4.0",
                    "framework_ref": f"e-CF:{code}",
                    "last_updated": "2026-01-01T00:00:00Z",
                },
            }
        )
    skill_pk = {code: i for i, (code, _, _) in enumerate(SKILLS, start=1)}

    for i, (name, issuer, _) in enumerate(CERTS, start=1):
        out.append(
            {
                "model": "skillzor.certification",
                "pk": i,
                "fields": {
                    "name": name,
                    "issuer": issuer,
                    "description": name,
                    "validity_period": "3 years",
                    "external_ref": "",
                    "last_updated": "2026-01-01T00:00:00Z",
                },
            }
        )

    emp_pk = es_pk = ec_pk = 0
    headcount = sum(count for _, _, count in ORG)
    names = rng.sample([(first, last) for first in FIRST for last in LAST], headcount)
    for dept, title, count in ORG:
        for _ in range(count):
            emp_pk += 1
            first, last = names[emp_pk - 1]
            out.append(
                {
                    "model": "skillzor.employee",
                    "pk": emp_pk,
                    "fields": {
                        "first_name": first,
                        "last_name": last,
                        "department": dept,
                        "job_title": title,
                        "last_updated": "2026-01-01T00:00:00Z",
                    },
                }
            )
            for code in SKILLS_BY_TITLE[title]:
                es_pk += 1
                out.append(
                    {
                        "model": "skillzor.employeeskill",
                        "pk": es_pk,
                        "fields": {
                            "employee": emp_pk,
                            "skill": skill_pk[code],
                            "proficiency_level": rng.randint(1, 5),
                            "last_updated": "2026-01-01T00:00:00Z",
                        },
                    }
                )
            for c_pk, (_, _, titles) in enumerate(CERTS, start=1):
                if title in titles and rng.random() < 0.8:
                    ec_pk += 1
                    out.append(
                        {
                            "model": "skillzor.employeecertification",
                            "pk": ec_pk,
                            "fields": {
                                "employee": emp_pk,
                                "certification": c_pk,
                                "issue_date": date(
                                    rng.randint(2019, 2025), rng.randint(1, 12), 1
                                ).isoformat(),
                                "expiration_date": None,
                                "last_updated": "2026-01-01T00:00:00Z",
                                "evidence": "",
                            },
                        }
                    )

    target = (
        Path(__file__).resolve().parents[1]
        / "undiscriminate"
        / "fixtures"
        / "demo_org.json"
    )
    target.write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {target} ({emp_pk} employees)")


if __name__ == "__main__":
    main()
