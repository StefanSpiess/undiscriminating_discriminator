.PHONY: install lint test check

install:
	pipenv install --dev

lint:
	pipenv run black .
	pipenv run flake8

test:
	pipenv run pytest -q

check: lint test
