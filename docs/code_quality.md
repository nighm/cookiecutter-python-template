# 代码质量指南

## 工具链概述

我们的代码质量工具链分为三个层次，每个层次都有其特定的用途和重要性。

### 基础层工具 (必须)

这些工具是最基本且必须运行的工具，用于快速发现和修复常见问题。

| 工具 | 用途 | 运行命令 | 配置位置 |
|------|------|----------|----------|
| Black | 代码格式化 | `black .` | `pyproject.toml` [tool.black] |
| isort | 导入语句排序 | `isort .` | `pyproject.toml` [tool.isort] |
| Ruff | 快速代码检查 | `ruff check .` | `pyproject.toml` [tool.ruff] |
| MyPy | 类型检查 | `mypy src tests` | `pyproject.toml` [tool.mypy] |
| pytest | 单元测试 | `pytest` | `pyproject.toml` [tool.pytest] |

### 标准层工具 (推荐)

这些工具提供更深入的代码分析，建议在提交代码前运行。

| 工具 | 用途 | 运行命令 | 特点 |
|------|------|----------|------|
| Pylint | 深度代码分析 | `pylint src tests` | 全面的代码检查和重构建议 |
| Bandit | 安全漏洞检查 | `bandit -r src` | 发现潜在安全问题 |
| Vulture | 死代码检测 | `vulture src` | 识别未使用的代码 |
| pytest-cov | 测试覆盖率 | `pytest --cov=src` | 生成覆盖率报告 |

### 高级层工具 (可选)

这些工具用于更深层次的代码质量分析，建议在重要版本发布前运行。

| 工具 | 用途 | 运行命令 | 特点 |
|------|------|----------|------|
| Safety | 依赖安全检查 | `safety check` | 检查已知漏洞 |
| Xenon | 代码复杂度检查 | `xenon --max-absolute A src` | 识别需要重构的代码 |
| Radon | 代码度量分析 | `radon cc src` | 计算圈复杂度 |

## 快速使用指南

### 一键运行所有检查

使用项目提供的脚本运行完整检查：
```bash
python scripts/run_quality_checks.py
```

### Git提交检查

项目已配置pre-commit hooks，包含基础层的所有工具：
```bash
# 安装hooks
pre-commit install

# 手动运行检查
pre-commit run --all-files
```

### 持续集成

在GitHub Actions中：
1. 基础层工具检查必须通过
2. 标准层工具作为警告报告
3. 高级层工具在发布时运行

## 最佳实践

### 1. 代码风格

- 使用Black格式化代码，保持一致的代码风格
- 使用isort保持导入语句整洁有序
- 遵循PEP 8规范
- 使用类型注解提高代码可读性

### 2. 测试规范

- 编写有意义的测试用例
- 使用pytest fixtures复用测试代码
- 保持测试简单、独立、可重复
- 维持高测试覆盖率（建议>80%）

### 3. 文档规范

- 为所有公共API编写文档字符串
- 包含代码示例
- 及时更新文档
- 使用类型注解

### 4. 安全实践

- 定期运行安全检查
- 及时更新依赖
- 避免硬编码敏感信息
- 使用环境变量管理配置

## 常见问题解决

### 1. 工具冲突处理

#### Black vs isort
解决：在isort配置中使用black配置文件
```toml
[tool.isort]
profile = "black"
```

#### Pylint vs Black
解决：在pylintrc中禁用格式相关检查
```toml
[tool.pylint.format]
max-line-length = 88  # 匹配Black
```

### 2. 性能优化

- 只对修改的文件运行检查：
  ```bash
  git diff --name-only | xargs poetry run black
  ```

- 使用缓存加速检查：
  ```bash
  pytest --cache-clear  # 清除缓存
  ```

### 3. 误报处理

- Pylint误报：
  ```python
  # pylint: disable=specific-error
  ```

- Mypy误报：
  ```python
  # type: ignore[error-code]
  ```

## 工具配置示例

### pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.11"
warn_return_any = true
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-ra -q" 