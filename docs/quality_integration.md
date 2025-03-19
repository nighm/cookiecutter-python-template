# 代码检查集成指南

## 一、集成方案概述

### 1.1 文件结构
```
{{cookiecutter.project_slug}}/
├── .github/
│   └── workflows/
│       ├── basic_check.yml     # 基础级别CI配置
│       ├── standard_check.yml  # 标准级别CI配置
│       └── advanced_check.yml  # 高级级别CI配置
├── scripts/
│   └── quality/
│       ├── basic_check.sh      # 基础检查脚本
│       ├── standard_check.sh   # 标准检查脚本
│       └── advanced_check.sh   # 高级检查脚本
└── config/
    └── quality/
        ├── basic/             # 基础级别配置文件
        │   ├── .flake8
        │   ├── .pylintrc
        │   └── mypy.ini
        ├── standard/         # 标准级别配置文件
        │   ├── .pylintrc
        │   └── bandit.yaml
        └── advanced/        # 高级级别配置文件
            ├── sonar.properties
            └── security.yaml
```

### 1.2 配置方式
在 `cookiecutter.json` 中添加质量检查级别选项：
```json
{
    "project_name": "Python Project",
    "quality_level": ["basic", "standard", "advanced"],
    "use_precommit": "y",
    "use_github_actions": "y"
}
```

## 二、自动化实现方案

### 2.1 本地开发环境配置

1. **Pre-commit钩子配置**
```yaml
# {{cookiecutter.project_slug}}/.pre-commit-config.yaml
{% if cookiecutter.quality_level == "basic" %}
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
{% endif %}

{% if cookiecutter.quality_level == "standard" %}
  # 包含basic的所有配置，并添加：
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.0
    hooks:
      - id: bandit
  - repo: https://github.com/PyCQA/pylint
    rev: v2.17.0
    hooks:
      - id: pylint
{% endif %}

{% if cookiecutter.quality_level == "advanced" %}
  # 包含standard的所有配置，并添加：
  - repo: local
    hooks:
      - id: security-checks
        name: Security Checks
        entry: bash -c 'poetry run bandit -r . && poetry run safety check'
        language: system
{% endif %}
```

2. **VS Code设置**
```json
# {{cookiecutter.project_slug}}/.vscode/settings.json
{
    "python.linting.enabled": true,
    {% if cookiecutter.quality_level == "basic" %}
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": false,
    {% endif %}
    {% if cookiecutter.quality_level in ["standard", "advanced"] %}
    "python.linting.pylintEnabled": true,
    "python.linting.banditEnabled": true,
    {% endif %}
    {% if cookiecutter.quality_level == "advanced" %}
    "python.linting.mypyEnabled": true,
    {% endif %}
}
```

### 2.2 CI/CD配置

1. **基础级别 GitHub Actions**
```yaml
# {{cookiecutter.project_slug}}/.github/workflows/basic_check.yml
name: Basic Quality Check
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install poetry
          poetry install
      - name: Run basic checks
        run: |
          poetry run black . --check
          poetry run isort . --check
          poetry run flake8
```

2. **标准级别 GitHub Actions**
```yaml
# {{cookiecutter.project_slug}}/.github/workflows/standard_check.yml
name: Standard Quality Check
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install poetry
          poetry install
      - name: Run standard checks
        run: |
          poetry run black . --check
          poetry run isort . --check
          poetry run flake8
          poetry run pylint src tests
          poetry run bandit -r .
          poetry run pytest --cov=src --cov-fail-under=80
```

3. **高级级别 GitHub Actions**
```yaml
# {{cookiecutter.project_slug}}/.github/workflows/advanced_check.yml
name: Advanced Quality Check
on: 
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install poetry
          poetry install
      - name: Run advanced checks
        run: |
          poetry run black . --check
          poetry run isort . --check
          poetry run flake8
          poetry run pylint src tests
          poetry run bandit -r .
          poetry run pytest --cov=src --cov-fail-under=95
          poetry run safety check
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## 三、自动运行时机

### 3.1 本地开发阶段
1. **编辑器实时检查**
   - VS Code配置自动在编辑时运行基础检查
   - 保存文件时触发格式化

2. **Git提交前检查**
   - Pre-commit钩子自动运行配置的检查
   - 可以通过 `git commit --no-verify` 跳过（不推荐）

### 3.2 代码审查阶段
1. **Pull Request触发**
   - GitHub Actions自动运行对应级别的检查
   - 检查结果显示在PR页面

2. **手动触发检查**
```bash
# 运行基础检查
poetry run poe check-basic

# 运行标准检查
poetry run poe check-standard

# 运行高级检查
poetry run poe check-advanced
```

### 3.3 发布阶段
1. **版本发布前检查**
   - 通过GitHub Actions在发布前运行完整检查
   - 生成质量报告和安全审计报告

2. **定期安全扫描**
   - 配置每周自动运行安全检查
   - 发现问题自动创建Issue

## 四、集成步骤

### 4.1 初始设置
1. 在创建项目时选择质量检查级别：
```bash
cookiecutter https://github.com/your-username/cookiecutter-python-template
# 根据提示选择 quality_level
```

2. 安装依赖：
```bash
cd your-project
poetry install
```

### 4.2 配置检查工具
1. 初始化pre-commit：
```bash
poetry run pre-commit install
```

2. 配置编辑器：
- VS Code会自动读取 `.vscode/settings.json`
- PyCharm需要手动启用相应的检查工具

### 4.3 CI/CD设置
1. 在GitHub仓库设置中：
- 启用GitHub Actions
- 配置必要的密钥（如SONAR_TOKEN）

2. 推送代码时：
- GitHub Actions会自动运行相应级别的检查
- 检查结果会在PR中显示

## 五、最佳实践建议

### 5.1 选择合适的级别
- 个人项目：基础级别
- 团队项目：标准级别
- 商业项目：高级级别

### 5.2 逐步提升要求
1. 先从基础级别开始
2. 团队适应后升级到标准级别
3. 需要时再升级到高级级别

### 5.3 维护和更新
1. 定期更新依赖版本
2. 根据团队反馈调整规则
3. 保持配置文件的同步 