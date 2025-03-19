# 代码质量工具配置指南

本文档详细说明了项目中各个代码质量工具的配置和使用方法。

## 基础级别工具配置

### Black 代码格式化
```toml
[tool.black]
line-length = 88
target-version = ["py38"]
include = '\.pyi?$'
```
使用方法：
```bash
poetry run black .  # 格式化所有Python文件
poetry run black src tests  # 格式化特定目录
```

### Ruff 代码检查
```toml
[tool.ruff]
line-length = 88
target-version = "py38"
select = ["E", "F", "B", "I"]  # 启用的规则
ignore = ["E203", "E501"]  # 忽略的规则

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # 忽略未使用的导入
```
使用方法：
```bash
poetry run ruff check .  # 检查代码
poetry run ruff check --fix .  # 自动修复问题
```

### isort 导入排序
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 88
```
使用方法：
```bash
poetry run isort .  # 排序所有文件
poetry run isort --check-only .  # 仅检查不修改
```

### MyPy 类型检查
```toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```
使用方法：
```bash
poetry run mypy src tests  # 类型检查
```

### PyDocStyle 文档检查
```toml
[tool.pydocstyle]
convention = "google"  # 使用Google风格文档
add_ignore = ["D100", "D104"]  # 忽略的规则
```
使用方法：
```bash
poetry run pydocstyle src  # 检查文档字符串
```

## 标准级别工具配置

### Pytest 测试配置
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=src --cov-report=term-missing"
pythonpath = ["."]
```
使用方法：
```bash
poetry run pytest  # 运行测试
poetry run pytest --cov=src --cov-report=html  # 生成HTML覆盖率报告
```

### Pylint 代码分析
```toml
[tool.pylint]
max-line-length = 88
disable = [
    "C0111",  # missing-docstring
    "R0903",  # too-few-public-methods
]
```
使用方法：
```bash
poetry run pylint src tests  # 运行代码分析
```

### Bandit 安全检查
```toml
[tool.bandit]
exclude_dirs = ["tests"]
skips = ["B101"]  # 跳过assert语句检查
```
使用方法：
```bash
poetry run bandit -r src  # 递归检查源代码
```

### Vulture 死代码检查
```toml
[tool.vulture]
min_confidence = 80
paths = ["src"]
exclude = ["tests"]
```
使用方法：
```bash
poetry run vulture src  # 检查死代码
```

## 高级级别工具配置

### Safety 依赖安全检查
使用方法：
```bash
poetry run safety check  # 检查依赖安全性
```

### Xenon 代码复杂度检查
使用方法：
```bash
poetry run xenon --max-absolute A src  # 检查代码复杂度
```

### Radon 代码质量度量
使用方法：
```bash
poetry run radon cc src  # 计算圈复杂度
poetry run radon mi src  # 计算可维护性指数
```

### PyType 类型检查
```toml
[tool.pytype]
inputs = ["src"]
python_version = "3.8"
```
使用方法：
```bash
poetry run pytype src  # 运行类型检查
```

### Scalene 性能分析
使用方法：
```bash
poetry run scalene src/your_script.py  # 分析性能
```

## 自动化检查配置

为了自动运行这些检查，我们可以使用pre-commit hooks。创建`.pre-commit-config.yaml`文件：

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
    rev: 24.0.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
    -   id: isort

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

安装和使用pre-commit：
```bash
# 安装pre-commit
poetry run pre-commit install

# 手动运行所有检查
poetry run pre-commit run --all-files
```

## 一键运行所有检查

为了方便运行所有检查，可以创建一个make命令或shell脚本：

```bash
#!/bin/bash
# run_checks.sh

echo "Running code quality checks..."

# 格式化和lint
poetry run black .
poetry run isort .
poetry run ruff check .

# 类型检查
poetry run mypy src tests

# 测试和覆盖率
poetry run pytest

# 安全检查
poetry run bandit -r src
poetry run safety check

# 代码质量度量
poetry run radon cc src
poetry run xenon --max-absolute A src

echo "All checks completed!"
```

使用方法：
```bash
chmod +x run_checks.sh
./run_checks.sh
``` 