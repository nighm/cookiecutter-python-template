.PHONY: help init test lint format clean docs

help:
	@echo "Available commands:"
	@echo "  init      Initialize development environment"
	@echo "  test      Run tests with coverage"
	@echo "  lint      Run code quality checks"
	@echo "  format    Format code"
	@echo "  clean     Clean temporary files"
	@echo "  docs      Build documentation"

init:
	poetry install
	poetry run pre-commit install
	poetry run pre-commit autoupdate

test:
	poetry run pytest

lint:
	poetry run black --check src tests
	poetry run isort --check-only src tests
	poetry run mypy src tests

format:
	poetry run black src tests
	poetry run isort src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

docs:
	cd docs && poetry run make html
