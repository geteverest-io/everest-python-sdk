.PHONY: help install install-dev test coverage lint format clean build upload

help:
	@echo "Available commands:"
	@echo "  make install        Install package"
	@echo "  make install-dev    Install package with dev dependencies"
	@echo "  make test          Run tests"
	@echo "  make coverage      Run tests with coverage report"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code with black"
	@echo "  make clean         Remove build artifacts"
	@echo "  make build         Build distribution packages"
	@echo "  make upload        Upload to PyPI (requires credentials)"

install:
	pip install -e .

install-dev:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=everest_api --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	flake8 everest_api/ tests/
	mypy everest_api/

format:
	black everest_api/ tests/ example.py example_webhook_endpoint.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*
