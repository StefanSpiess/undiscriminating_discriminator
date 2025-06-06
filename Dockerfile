# Dockerfile for Undiscriminating Discriminator
# Based on Python 3.12 slim image with best practices

FROM python:3.12-slim

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy Pipfile and lock for dependency installation
COPY Pipfile Pipfile.lock /app/

# Install pipenv and project dependencies in one layer
RUN pip install --no-cache-dir pipenv \
    && PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system --ignore-pipfile

# Copy project files
COPY . /app

# Collect static files (if configured)
# RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Start the application using a production-ready server
CMD ["gunicorn", "undiscriminate.wsgi:application", "--bind", "0.0.0.0:8000"]
