# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## 功能特点

- 完整的代码质量检查工具链
- 类型检查和文档字符串验证
- 自动化测试和覆盖率报告
- 性能分析和优化工具
- 安全性检查

## 快速开始

1. 确保已安装 Python 3.8 或更高版本
2. 安装 Poetry 包管理工具：
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. 安装项目依赖：
   ```bash
   poetry install
   ```

4. 运行测试：
   ```bash
   poetry run pytest
   ```

5. 运行代码质量检查：
   ```bash
   poetry run black .
   poetry run isort .
   poetry run ruff check .
   poetry run mypy .
   ```

## 代码质量工具

### 基础工具
- **black**: 代码格式化
- **isort**: 导入语句排序
- **ruff**: 快速的 Python linter
- **mypy**: 类型检查
- **pydocstyle**: 文档字符串检查
- **pytest**: 测试框架

### 标准工具
- **pytest-cov**: 测试覆盖率
- **pylint**: 代码分析
- **bandit**: 安全检查
- **vulture**: 死代码检查

### 高级工具
- **safety**: 依赖安全检查
- **xenon**: 代码复杂度检查
- **radon**: 代码质量度量
- **pytype**: 补充类型检查
- **scalene**: 性能分析

## 使用指南

### 运行所有检查

```bash
# 运行所有基础检查
poetry run black . && poetry run isort . && poetry run ruff check . && poetry run mypy .

# 运行测试和覆盖率报告
poetry run pytest --cov

# 运行安全检查
poetry run bandit -r src
poetry run safety check

# 运行性能分析
poetry run scalene src/main.py
```

### 配置文件

- `pyproject.toml`: 主要配置文件，包含所有工具的设置
- `.gitignore`: Git 忽略文件配置
- `tests/`: 测试文件目录
- `src/`: 源代码目录

## 开发流程

1. 创建新功能分支
2. 编写代码和测试
3. 运行代码质量检查
4. 提交代码前确保所有检查通过
5. 创建合并请求

## 贡献指南

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建合并请求

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 作者

{{ cookiecutter.full_name }} <{{ cookiecutter.email }}> 