# Undiscriminating Discriminator

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview
Undiscriminating Discriminator is an MVP prototype exploring a least-discriminating multi-model approach for AI-driven HR skill management. It provides a RESTful interface to manage employees, skills, certifications, projects, budgets, and development actions, facilitating experimentation with fair, multi-framework competency models.

### Features
- CRUD operations for Employees, Skills, Certifications, Projects, Budgets, and Development Actions via Django REST framework.
- Data fixtures for rapid testing and demonstration.
- Modular design supporting extension with additional AI/ML models and fairness frameworks.

## LLM Code Assistant Collaboration
This repository is designed for iterative development with LLM-based code assistant agents. Guidelines for maintainers and agents reside in [AGENTS.md](AGENTS.md). Additional context is stored in `background/` and plugin documentation in `plugins/`. These directories are development-only resources and should be excluded from runtime containers.

## Tech Stack
- Python 3.12
- Django 5.2
- Django REST framework
- SQLite (default; easily configurable for PostgreSQL/MySQL)
- Pytest for testing
- Black for code formatting

## Prerequisites
- Git
- Python 3.12
- Pipenv (or `venv` and `pip`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/undiscriminating_discriminator.git
   cd undiscriminating_discriminator
   ```
2. Install dependencies with Pipenv:
   ```bash
   pipenv install --dev
   pipenv shell
   ```
   *Alternatively, use `python -m venv env && source env/bin/activate && pip install -r requirements.txt`.*
3. Configure environment variables: create a `.env` file in the project root (see `.env.example`):
   ```ini
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```
   If `SECRET_KEY` is missing and `DEBUG` is `True`, a development placeholder is used
   and a warning is logged using Django's logging system. When `DEBUG` is `False`, `SECRET_KEY` must be set or the
   application will fail to start.
4. Apply migrations and load sample data:
   ```bash
   python manage.py migrate
   python manage.py loaddata fixtures/sample_data.json
   ```

## Running the Application
Start the development server:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/api/` for the API root, or navigate to specific endpoints (see **API Endpoints** below).

## Frontend Authentication Example
An example login form using the OAuth2 *password* grant is provided in
`frontend/index.html`.
Serve the `frontend` directory via `python -m http.server 9000` (or any other
port) and open `http://localhost:9000/index.html` in a browser.
The form posts the user's credentials to `/o/token/` and displays the returned
access token. This flow is intended for local testing only and should not be
used in production.

## API Endpoints
| Resource                 | Endpoint                       | Methods       |
| ------------------------ | ------------------------------ | ------------- |
| Employees                | `/api/employees/`              | GET, POST     |
| Employee Detail          | `/api/employees/{id}/`         | GET, PUT, DELETE |
| Skills                   | `/api/skills/`                 | GET, POST     |
| Certifications           | `/api/certifications/`         | GET, POST     |
| Projects                 | `/api/projects/`               | GET, POST     |
| Budgets                  | `/api/budgets/`                | GET, POST     |
| Development Actions      | `/api/development-actions/`    | GET, POST     |

## Testing
Run the full test suite with coverage:
```bash
pytest --cov=.
```  
Ensure code is formatted and linted:
```bash
black --check .
```
Alternatively, use the included `Makefile`:
```bash
make install  # install dependencies with Pipenv
make check    # run black, flake8, and tests
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository and create a feature branch (`git checkout -b feature/my-feature`).
2. Commit your changes (`git commit -am 'Add new feature'`).
3. Ensure all tests pass and code is formatted (`pytest`, `black`).
4. Push to the branch (`git push origin feature/my-feature`) and submit a Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
