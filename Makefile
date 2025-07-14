.PHONY: install lint test build clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  install  - Install project dependencies"
	@echo "  lint     - Run code linting and formatting checks"
	@echo "  test     - Run test suite"
	@echo "  build    - Build the package"
	@echo "  clean    - Clean build artifacts"
	@echo "  help     - Show this help message"

install:
	@echo "Installing project dependencies..."
	[ -d .venv ] || python -m venv .venv
	. .venv/bin/activate && \
	  pip install --upgrade pip && \
	  pip install -e .[test,build] && \
	  pre-commit install && \
	  pre-commit install-hooks

lint:
	@echo "Running linting and formatting checks..."
	. .venv/bin/activate && pre-commit run --all-files

test:
	@echo "Running test suite..."
	. .venv/bin/activate && pytest --cov=inter

build:
	@echo "Building package..."
	. .venv/bin/activate && flit build

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
