# Agent Instructions

This file is the contract for every coding agent (Codex, Claude Code, Copilot, …)
and every human working on this repository.

## Collaboration Overview
- You are an expert in Django REST framework.
- Maintain a strong focus on security. Implement best practices for authentication, authorization, and secure coding.
- Avoid structural bias in data models and consider accessibility in API design.

## Privacy invariants (never break these)
1. **No demographic fields.** Do not add age, birth date, gender, nationality,
   ethnicity, photo, marital status or similar fields to any model. If a feature
   seems to need one, stop and ask.
2. **The AI export is the only way out.** Skill data for AI/analytics leaves the
   system only through `skillzor/privacy.py` (`/api/ai-export/`). Do not add
   other bulk or analytics endpoints that return employee-level data.
3. **Never export direct identifiers.** Names, free-text fields (`evidence`,
   `description` on person-related records) and exact dates must not appear in
   the export. New fields on `Employee`, `EmployeeSkill` or
   `EmployeeCertification` are excluded from the export unless explicitly
   reviewed.
4. **k-anonymity must hold.** Every released `(department, job_title)` bucket
   has at least `k` members. `test_every_released_bucket_has_at_least_k_members`
   must keep passing; do not weaken or skip it.
5. **Reads need permissions too.** Keep `StrictModelPermissions` as the default
   permission class. The export keeps its own dedicated permission.
6. **Limits stay documented.** If you change what the export does, update
   `docs/ai_export.md`, including the "Known limits" section.

## Setup & Workflow
1. Install dependencies:
   ```bash
   pipenv install --dev
   ```
2. Format, lint and scan:
   ```bash
   pipenv run black .
   pipenv run flake8
   pipenv run bandit -r undiscriminate scripts -x "*/tests/*"
   ```
3. Run tests (coverage must stay ≥ 90 %):
   ```bash
   pipenv run pytest --cov=undiscriminate --cov-fail-under=90
   ```
4. Fix any `bandit` findings before committing. Only suppress a finding with a
   targeted `# nosec BXXX` when it is a verified false positive.
5. Apply database migrations whenever models change (from `undiscriminate/`):
   ```bash
   pipenv run python manage.py makemigrations
   pipenv run python manage.py migrate
   ```
6. If you change models used by the demo data, regenerate it:
   ```bash
   python scripts/generate_demo_fixture.py
   ```

## Definition of done
A task is done when all CI gates in `.github/workflows/python-app.yml` pass
locally, new behaviour has tests, and the README or docs reflect the change.
Saying "done" without running the gates does not count.

## Commit Guidelines
- Write concise commit messages in the imperative mood (e.g. "Add user API").
- Keep changes focused and grouped logically.
- Ensure `black`, `flake8`, `bandit`, and `pytest` pass before committing.
- When adding dependencies, update both `Pipfile` and `Pipfile.lock`. Runtime
  dependencies go in `[packages]`, tooling in `[dev-packages]`.

## Knowledge Base
- `background/` contains domain PDFs and notes.
- `plugins/` stores plugin documentation and configuration.
- `docs/ai_export.md` documents the export's guarantees and limits.

**Note:** AGENTS.md and the contents of `background/`, `plugins/`, `docs/` and
`scripts/` are for maintainers only. They are excluded from the container image
via `.dockerignore`.
