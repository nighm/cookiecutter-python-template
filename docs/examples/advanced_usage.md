# 高级使用示例

本文档展示了如何使用项目模板创建一个实际的Python项目。

## 1. 环境准备

### 1.1 创建工作目录

首先，我们需要创建一个专门的工作目录来存放项目：

**Windows:**
```powershell
# 获取用户目录路径
$userProfile = $env:USERPROFILE

# 创建并切换到projects目录
$projectsPath = Join-Path $userProfile "projects"
if (-not (Test-Path $projectsPath)) {
    New-Item -ItemType Directory -Path $projectsPath
}
Set-Location $projectsPath
```

**Linux/MacOS:**
```bash
# 切换到用户目录
cd ~

# 创建projects目录（如果不存在）
mkdir -p projects

# 切换到projects目录
cd projects
```

### 1.2 安装必要工具

**Windows:**
```powershell
# 安装 Python 3.11
pyenv install 3.11.8
pyenv local 3.11.8

# 安装 Poetry（PowerShell）
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# 安装 cookiecutter
pip install cookiecutter
```

**Linux/MacOS:**
```bash
# 安装 Python 3.11
pyenv install 3.11.8
pyenv local 3.11.8

# 安装 Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 安装 cookiecutter
pip install cookiecutter
```

## 2. 项目创建

### 2.1 使用模板创建项目

**Windows:**
确保你当前在正确的工作目录下（%USERPROFILE%\projects），然后执行：

```powershell
# 创建新项目
cookiecutter gh:nighm/cookiecutter-python-template
```

**Linux/MacOS:**
确保你当前在正确的工作目录下（~/projects），然后执行：

```bash
# 创建新项目
cookiecutter gh:nighm/cookiecutter-python-template
```

项目配置示例（所有系统通用）：
```
project_name [My Project]: data_processor
project_slug [data_processor]: data_processor
project_description [A Python project]: 一个高性能的数据处理服务
author_name [Your Name]: Your Name
author_email [your.email@example.com]: your.email@example.com
python_version [3.11]: 3.11
use_docker [y]: y
use_github_actions [y]: y
```

### 1.2 项目结构

生成的项目结构如下：

```
├── src/                    # 源代码目录
│   └── {{cookiecutter.project_slug}}/
│       ├── __init__.py
│       ├── core/          # 核心功能模块
│       ├── models/        # 数据模型
│       └── utils/         # 工具函数
├── tests/                  # 测试文件
│   ├── __init__.py
│   ├── conftest.py        # pytest配置
│   └── quality_examples/  # 质量检查示例
├── docs/                   # 文档
│   ├── en/                # 英文文档
│   │   └── source/
│   └── zh/                # 中文文档
│       └── source/
├── scripts/                # 工具脚本
│   └── run_quality_checks.py
├── .github/               # GitHub Actions 配置
│   └── workflows/
│       ├── ci.yml        # CI工作流
│       ├── docs.yml      # 文档部署工作流
│       ├── release.yml   # 发布工作流
│       └── changelog.yml # 更新日志工作流
├── .pytest_cache/        # pytest缓存
├── pyproject.toml        # Poetry 项目配置
├── poetry.lock          # Poetry 依赖锁定文件
├── README.md            # 项目说明
├── CHANGELOG.md         # 更新日志
└── CONTRIBUTING.md      # 贡献指南
```

## 2. 项目配置

### 2.1 依赖管理 (pyproject.toml)

```toml
[tool.poetry]
name = "data_processor"
version = "0.1.0"
description = "一个高性能的数据处理服务"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = ">=3.11,<3.12"
pydantic = "^2.6.3"
python-dotenv = "^1.0.1"
structlog = "^24.1.0"
sqlalchemy = "^2.0.27"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.1"
pytest-cov = "^4.1.0"
pytest-asyncio = "^0.23.5"
black = "^24.2.0"
ruff = "^0.3.0"
mypy = "^1.8.0"
bandit = "^1.7.7"
isort = "^5.13.2"
pre-commit = "^3.6.2"

[tool.poetry.group.docs.dependencies]
sphinx = "^7.2.6"
sphinx-rtd-theme = "^2.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
```

### 2.2 代码质量工具配置 (.pre-commit-config.yaml)

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
    -   id: black

-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
    -   id: ruff
        args: [--fix]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-all]
```

## 3. 代码质量检查

项目支持三个级别的代码质量检查：

### 3.1 基础级别 (Basic)

```bash
# 运行基础代码质量检查
poetry run python scripts/run_quality_checks.py --level basic
```

包含：

- Black 代码格式化
- Ruff 基础检查
- MyPy 类型检查

### 3.2 标准级别 (Standard)

```bash
# 运行标准代码质量检查
poetry run python scripts/run_quality_checks.py --level standard
```

包含：

- 基础级别的所有检查
- Bandit 安全检查
- 更严格的 Ruff 规则

### 3.3 高级级别 (Advanced)

```bash
# 运行高级代码质量检查
poetry run python scripts/run_quality_checks.py --level advanced
```

包含：

- 标准级别的所有检查
- 复杂度分析
- 文档完整性检查
- 更多自定义规则

## 4. CI/CD配置

### 4.1 GitHub Actions工作流

项目包含三个主要的工作流：

1. **CI工作流** (.github/workflows/ci.yml)
   
   - 运行测试
   - 代码质量检查
   - 覆盖率报告

2. **文档部署工作流** (.github/workflows/docs.yml)
   
   - 构建文档
   - 部署到 GitHub Pages

3. **发布工作流** (.github/workflows/release.yml)
   
   - 版本标签触发
   - 自动发布到 PyPI

## 5. 使用说明

### 5.1 开发环境设置

**Windows:**
```powershell
# 安装 Python 3.11
pyenv install 3.11.8
pyenv local 3.11.8

# 安装 Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# 安装依赖
poetry install

# 安装pre-commit钩子
poetry run pre-commit install
```

**Linux/MacOS:**
```bash
# 安装 Python 3.11
pyenv install 3.11.8
pyenv local 3.11.8

# 安装 Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 安装依赖
poetry install

# 安装pre-commit钩子
poetry run pre-commit install
```

### 5.2 运行测试

所有系统通用：
```bash
# 运行所有测试
poetry run pytest

# 运行带覆盖率报告的测试
poetry run pytest --cov=src --cov-report=html

# 运行特定测试文件
poetry run pytest tests/test_specific.py -v
```

### 5.3 文档构建

所有系统通用：
```bash
# 构建英文文档
cd docs/en && poetry run make html

# 构建中文文档
cd docs/zh && poetry run make html

# 本地预览文档
poetry run python -m http.server --directory docs/_build/html 8000
```

## 6. 最佳实践

1. **版本控制**
   
   - 使用语义化版本号
   - 保持更新日志（CHANGELOG.md）的及时更新
   - 使用分支策略（main/develop/feature/hotfix）

2. **代码质量**
   
   - 使用 `pyproject.toml` 统一管理工具配置
   - 运行完整的质量检查套件
   - 保持测试覆盖率在 80% 以上

3. **依赖管理**
   
   - 使用 Poetry 管理依赖
   - 定期更新依赖版本
   - 使用依赖分组（main/dev/docs）

4. **文档维护**
   
   - 使用 Sphinx 生成文档
   - 提供中英文文档
   - 包含详细的 API 文档和示例

## 7. 常见问题

1. **Poetry安装依赖失败**
   
   ```bash
   # 清理缓存后重试
   poetry cache clear . --all
   poetry install
   ```

2. **pre-commit检查不通过**
   
   ```bash
   # 手动运行检查
   poetry run pre-commit run --all-files
   ```

3. **Ruff检查报错**
   
   ```bash
   # 自动修复 Ruff 报告的问题
   poetry run ruff check --fix .
   ```

4. **文档构建失败**
   
   ```bash
   # 清理构建目录后重试
   cd docs/en && poetry run make clean html
   ```

## 8. 更新日志

请参考项目根目录下的 [CHANGELOG.md](../CHANGELOG.md) 文件。