# Welcome to {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Getting Started

### Prerequisites

- Python {{ cookiecutter.python_version }} or higher
- Poetry for dependency management

### Installation

1. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd {{ cookiecutter.project_slug }}
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

## Development

### Code Quality

We use several tools to ensure code quality:

{% if cookiecutter.use_black == 'y' %}
- **Black** for code formatting
{% endif %}
{% if cookiecutter.use_mypy == 'y' %}
- **MyPy** for static type checking
{% endif %}
- **isort** for import sorting
- **pre-commit** for automated checks

### Testing

{% if cookiecutter.use_pytest == 'y' %}
We use pytest for testing. To run tests:

```bash
poetry run pytest
```
{% endif %}

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── src/
│   └── {{ cookiecutter.package_name }}/
│       ├── core/
│       ├── utils/
│       └── config/
├── tests/
├── docs/
└── README.md
```

# 项目文档

## 配置指南
- [代码质量配置](code_quality_config.md)
- [代码质量示例](quality_examples.md)

## 项目说明
- [项目概述](../README.md)
- [更新日志](../CHANGELOG.md)

## 外部文档
- [项目模板文档](../../docs/index.md)
- [代码质量工具指南](../../docs/code_quality_tools.md)
- [代码检查分级指南](../../docs/quality_levels.md) 