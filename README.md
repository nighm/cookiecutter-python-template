# Python Project Template

A modern, feature-rich Python project template using Cookiecutter.

## Features

- 🐍 Modern Python development with Poetry
- ✨ Code quality tools (Black, MyPy, isort)
- 🧪 Automated testing with pytest
- 🚀 Continuous Integration with GitHub Actions
- 📚 Comprehensive documentation with MkDocs
- 🐳 Optional Docker support
- 🔧 Optional Makefile support
- 🌟 Best practices out of the box

## Requirements

- Python 3.8+
- Cookiecutter
- Poetry (optional, but recommended)

## Usage

1. Install Cookiecutter:
   ```bash
   pip install cookiecutter
   ```

2. Generate a new project:
   ```bash
   cookiecutter gh:your-username/python-project-template
   ```

3. Answer the prompts to customize your project:
   - `project_name`: Your project's name
   - `project_slug`: The project's directory name
   - `author`: Your name
   - `email`: Your email
   - `description`: A short description of your project
   - `python_version`: Python version to use
   - Various feature flags (pytest, black, mypy, etc.)

## Options

- `use_pytest`: Include pytest for testing
- `use_black`: Include Black for code formatting
- `use_mypy`: Include MyPy for type checking
- `use_pre_commit`: Set up pre-commit hooks
- `use_docker`: Include Docker support
- `use_make`: Include Makefile
- `use_github_actions`: Include GitHub Actions workflows
- `use_mkdocs`: Include MkDocs documentation
- `include_examples`: Include example code
- `open_source_license`: Choose a license

## Project Structure

```
your-project/
├── src/
│   └── your_package/
│       ├── core/
│       ├── utils/
│       └── config/
├── tests/
├── docs/
├── docker/           # Optional
├── .github/
├── pyproject.toml
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This template is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
