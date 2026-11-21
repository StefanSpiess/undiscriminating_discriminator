# Production image for Undiscriminating Discriminator
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=False

WORKDIR /app

# Install only runtime dependencies from the lock file (no dev tools).
COPY Pipfile Pipfile.lock /app/
RUN pip install --no-cache-dir pipenv \
    && pipenv install --deploy --system --ignore-pipfile \
    && pip uninstall -y pipenv

COPY undiscriminate/ /app/undiscriminate/

# Run as an unprivileged user.
RUN useradd --create-home --uid 10001 app \
    && mkdir -p /app/undiscriminate/staticfiles \
    && chown -R app:app /app
USER app

WORKDIR /app/undiscriminate
EXPOSE 8000

# SECRET_KEY, PSEUDONYM_KEY and ALLOWED_HOSTS must be provided at runtime.
CMD ["gunicorn", "undiscriminate.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
