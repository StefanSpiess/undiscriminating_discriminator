# Agent Instructions

## Collaboration Overview
- You are an expert in Django REST framework.
- When modifying models, always create and apply migrations (`pipenv run python manage.py makemigrations` and `pipenv run python manage.py migrate`).
- Maintain a strong focus on security. Implement best practices for authentication, authorization, and secure coding.
- Avoid structural bias in data models and consider accessibility in API design.

## Setup
1. Install dependencies:
   ```bash
   pipenv install --dev
   ```
2. Run formatting and static checks:
   ```bash
   pipenv run black .
   pipenv run flake8
   ```
3. Run tests:
   ```bash
   pipenv run pytest
   ```

## Knowledge Base
- `background/` contains domain PDFs and notes.
- `plugins/` stores plugin documentation and configuration.

**Note:** AGENTS.md and the contents of `background/` and `plugins/` are for maintainers only. Ensure they are excluded from production container images.
