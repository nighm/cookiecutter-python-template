# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Features

- Modern Python development with Poetry
- Code quality tools (Black, MyPy, isort)
- Automated testing with pytest
- Continuous Integration with GitHub Actions
- Comprehensive documentation with MkDocs

## Installation

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

## Development

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run type checks
poetry run mypy .

# Format code
poetry run black .
```

## Documentation

```bash
# Build documentation
poetry run mkdocs build

# Serve documentation locally
poetry run mkdocs serve
```

## License

{% if cookiecutter.open_source_license != "Not open source" %}
This project is licensed under the {{ cookiecutter.open_source_license }} - see the [LICENSE](LICENSE) file for details.
{% else %}
This project is not open source and is intended for private use only.
{% endif %} 