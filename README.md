# Undiscriminating Discriminator

[![CI](https://github.com/StefanSpiess/undiscriminating_discriminator/actions/workflows/python-app.yml/badge.svg)](https://github.com/StefanSpiess/undiscriminating_discriminator/actions/workflows/python-app.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**A skills database that is built to feed AI systems without letting them see who people are.**

HR teams want AI for skill matching, staffing and development planning. The
fastest way to get a biased model is to train it on data that contains names,
demographics and other proxies. This project goes the other way: it stores the
minimum, describes competences in a standard vocabulary (the European
e-Competence Framework, e-CF, standardised as EN 16234-1),
and offers a single, privacy-preserving export for anything downstream.

## What it does

* **Skill profiles on a common scale.** Employees, skills, certifications,
  projects, budgets and development actions via a Django REST API. Skills
  reference e-CF competences (`e-CF:B.1`); proficiency follows the e-CF levels
  1–5 and is validated as such.
* **No demographics by design.** The data model has no fields for age, gender,
  nationality or similar. You can't leak what you don't store.
* **Pseudonymised, k-anonymised AI export.** `GET /api/ai-export/` releases
  skill profiles with HMAC pseudonyms instead of names, generalises job titles
  and departments until every group has at least *k* members, and drops rare
  skills that would single someone out. Guarantees *and limits* are written
  down in [docs/ai_export.md](docs/ai_export.md).
* **Need-to-know access.** Every endpoint requires the matching Django model
  permission, reads included. The export needs its own permission on top.
* **OAuth 2.0 per RFC 9700.** All Security BCP gates of django-oauth-toolkit are
  enforced in production; legacy flows only work in `DEBUG` for the local demo.

## Quickstart

```bash
pipenv install --dev
cd undiscriminate
pipenv run python manage.py migrate
pipenv run python manage.py loaddata fixtures/demo_org.json   # fictional company, 33 people
pipenv run python manage.py createsuperuser
pipenv run python manage.py runserver
```

Log in at `http://127.0.0.1:8000/admin/`, then open
`http://127.0.0.1:8000/api/ai-export/`. The demo company is built so that every
anonymisation rule fires at least once (lone architect, a department of exactly
five, two departments too small to stand alone, a skill only one person has).
Regenerate it with `python scripts/generate_demo_fixture.py`.

## API

| Resource | Endpoint |
| --- | --- |
| Employees | `/api/employees/` |
| Skills | `/api/skills/` |
| Employee skills (proficiency) | `/api/employee-skills/` |
| Certifications | `/api/certifications/` |
| Employee certifications | `/api/employee-certifications/` |
| Projects | `/api/projects/` |
| Budgets | `/api/budgets/` |
| Development actions | `/api/development-actions/` |
| **AI export** | `/api/ai-export/?k=5` |

All resources support the usual list/detail/create/update/delete routes.

## Configuration

| Variable | Required in production | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | yes | Django secret |
| `PSEUDONYM_KEY` | yes | HMAC key for export pseudonyms. Rotate to unlink old exports. |
| `ALLOWED_HOSTS` | yes | Comma-separated host names |
| `DEBUG` | – | `True` only for local development (the Docker image sets `False`) |
| `EXPORT_MIN_K` | – | Minimum group size for the export (default `5`) |
| `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS` | – | TLS hardening, on by default when `DEBUG=False` |

Run it in a container:

```bash
docker build -t undiscriminating-discriminator .
docker run -p 8000:8000 \
  -e SECRET_KEY=... -e PSEUDONYM_KEY=... -e ALLOWED_HOSTS=localhost \
  undiscriminating-discriminator
```

## Quality gates

Every push runs, and must pass:

```bash
pipenv run black --check .
pipenv run flake8
pipenv run bandit -r undiscriminate scripts -x "*/tests/*"
pipenv run python manage.py makemigrations --check      # in undiscriminate/
pipenv run python manage.py check --deploy --fail-level WARNING
pipenv run pytest --cov=undiscriminate --cov-fail-under=90
```

plus a Docker build. The k-anonymity guarantee is covered by a property test
over 300 random org charts. To check that the test actually bites, the
folding step was disabled once during development: 201 of the 300 cases failed.

## How this was built: agentic engineering

This repository is also an experiment in building software with coding agents
while keeping a human in charge of intent and quality.

1. **Research first.** The data model started as a literature-backed design
   note on competency standards (e-CF, IEEE RCD, Open Badges) and bias
   mitigation, kept in [`background/`](background/).
2. **A contract for agents.** [`AGENTS.md`](AGENTS.md) tells any agent how to
   set up, which gates must pass, and which privacy invariants must never be
   broken. Tools that read `AGENTS.md` (Codex, Claude Code, Copilot) all get
   the same rules.
3. **Agents do the work, in reviewable slices.** The first iteration was
   built in 10 days, mostly through small pull requests opened by OpenAI
   Codex: 14 of the first 17 merged PRs. The privacy-preserving export,
   permission model and hardening were added in a later pass with Claude Code.
4. **Machines check machines.** Formatting, linting, static security
   analysis, Django deploy checks, migrations, coverage and a property test
   are enforced in CI, so an agent can't "finish" a task by just claiming it's
   done.
5. **Humans own the trade-offs.** Agents are good at implementing a rule;
   deciding what *k* should be, or whether an export is acceptable at all, is
   documented as a human decision ([docs/ai_export.md](docs/ai_export.md#known-limits)).

## Project layout

```
undiscriminate/            Django project
  skillzor/                app: models, API, permissions
    privacy.py             pseudonymisation and k-anonymity
  fixtures/demo_org.json   fictional demo company
scripts/                   fixture generator
docs/                      export guarantees, deployment notes
background/                design research (not shipped in the image)
frontend/                  minimal OAuth login demo (local only)
AGENTS.md                  instructions for coding agents
```

## License

MIT, see [LICENSE](LICENSE).
