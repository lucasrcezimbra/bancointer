.PHONY: install lint test coverage

install:
	poetry install

lint:
	pre-commit run -a

test:
	pytest

coverage:
	pytest --cov=inter