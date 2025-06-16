# Agent Instructions

## Collaboration Overview
- You are an expert in Django REST framework.
- Maintain a strong focus on security. Implement best practices for authentication, authorization, and secure coding.
- Avoid structural bias in data models and consider accessibility in API design.

## Setup & Workflow
1. Install dependencies:
   ```bash
   pipenv install --dev
   ```
2. Format and lint:
   ```bash
   pipenv run black .
   pipenv run flake8
   pipenv run bandit -r .
   ```
3. Run tests:
   ```bash
   pipenv run pytest
   ```
4. Fix any `bandit` findings before committing.

5. Apply database migrations whenever models change:
   ```bash
   pipenv run python manage.py makemigrations
   pipenv run python manage.py migrate
   ```

## Commit Guidelines
- Write concise commit messages in the imperative mood (e.g. "Add user API").
- Keep changes focused and grouped logically.
- Ensure `black`, `flake8`, `bandit`, and `pytest` pass before committing.
- When adding dependencies, update both `Pipfile` and `Pipfile.lock`.

## Knowledge Base
- `background/` contains domain PDFs and notes.
- `plugins/` stores plugin documentation and configuration.

**Note:** AGENTS.md and the contents of `background/` and `plugins/` are for maintainers only. Ensure they are excluded from production container images.
