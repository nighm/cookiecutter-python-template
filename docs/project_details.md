# 项目详细说明

## 项目结构说明

### 目录结构
```
project_root/
├── src/                    # 源代码目录
│   └── your_package/       # 主包目录
│       ├── __init__.py    # 包初始化文件
│       ├── core/          # 核心功能模块
│       ├── utils/         # 工具函数
│       └── cli/           # 命令行接口
├── tests/                 # 测试目录
│   ├── __init__.py
│   ├── conftest.py       # pytest配置和通用fixture
│   └── test_*.py         # 测试文件
├── docs/                  # 文档目录
│   ├── index.md          # 文档首页
│   └── *.md              # 其他文档
├── scripts/              # 工具脚本
│   └── run_quality_checks.py  # 代码质量检查脚本
├── .github/              # GitHub配置
│   └── workflows/        # GitHub Actions工作流
├── config/              # 配置文件目录
│   └── quality/         # 代码质量工具配置
├── .env.example         # 环境变量示例
├── .gitignore          # Git忽略配置
├── .pre-commit-config.yaml  # pre-commit配置
├── CHANGELOG.md        # 更新日志
├── CONTRIBUTING.md     # 贡献指南
├── LICENSE            # 许可证
├── Makefile          # 常用命令
├── README.md         # 项目说明
├── mkdocs.yml        # 文档配置
├── poetry.lock       # 依赖版本锁定
├── poetry.toml       # Poetry配置
└── pyproject.toml    # 项目配置
```

### 关键文件说明

#### 1. pyproject.toml
项目的核心配置文件，包含：
- 项目元数据
- 依赖管理
- 构建系统配置
- 工具配置（black, mypy等）

```toml
[tool.poetry]
name = "your_package"
version = "0.1.0"
description = "项目描述"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "your_package", from = "src"}]

[tool.poetry.dependencies]
python = ">=3.11.0,<3.12.0"
# 其他依赖...

[tool.poetry.group.dev.dependencies]
# 开发依赖...

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# 工具配置...
[tool.black]
line-length = 88
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
```

#### 2. .pre-commit-config.yaml
Git提交钩子配置，用于自动运行代码质量检查：
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

# 其他钩子...
```

#### 3. mkdocs.yml
文档配置文件：
```yaml
site_name: 项目名称
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
```

## 开发工具链

### 1. 依赖管理 (Poetry)
- 虚拟环境管理
- 依赖解析和锁定
- 包发布工具

常用命令：
```bash
# 添加依赖
poetry add package_name
poetry add -D package_name  # 开发依赖

# 更新依赖
poetry update

# 构建和发布
poetry build
poetry publish
```

### 2. 代码质量工具
- 格式化：black, isort
- 静态检查：mypy, ruff
- 测试：pytest
- 覆盖率：pytest-cov
- 安全：bandit, safety

### 3. 文档工具 (MkDocs)
- Material主题
- Python API文档生成
- 自动部署到GitHub Pages

### 4. CI/CD (GitHub Actions)
- 自动测试
- 代码质量检查
- 文档部署
- 包发布

## 配置说明

### 1. 环境变量
项目使用 `.env` 文件管理环境变量：
```bash
# .env.example
DEBUG=false
LOG_LEVEL=INFO
API_KEY=your_api_key
```

### 2. 日志配置
```python
# src/your_package/utils/logging.py
import logging

def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
```

### 3. 测试配置
```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def test_data_dir() -> Path:
    return Path(__file__).parent / "data"
```

## 开发流程

### 1. 功能开发
1. 创建功能分支
2. 编写代码和测试
3. 运行代码质量检查
4. 提交PR

### 2. 测试流程
1. 单元测试（pytest）
2. 集成测试
3. 代码覆盖率检查
4. 性能测试（可选）

### 3. 发布流程
1. 更新版本号
2. 更新CHANGELOG
3. 创建发布分支
4. 运行完整测试
5. 构建和发布

## 最佳实践

### 1. 代码组织
- 使用清晰的模块结构
- 保持函数和类的单一职责
- 使用类型注解
- 编写清晰的文档字符串

### 2. 测试实践
- 编写有意义的测试用例
- 使用fixture复用测试代码
- 模拟外部依赖
- 保持测试简单明了

### 3. 文档实践
- 及时更新文档
- 包含代码示例
- 说明配置选项
- 提供故障排除指南

### 4. 版本控制
- 使用语义化版本
- 编写清晰的提交信息
- 及时合并上游更改
- 定期清理分支

## 常见问题

### 1. 环境问题
Q: 虚拟环境不生效？
A: 确保已运行 `poetry shell` 或使用 `poetry run`

### 2. 依赖问题
Q: 依赖冲突如何解决？
A: 检查 `poetry.lock`，使用 `poetry show --tree` 分析依赖树

### 3. 测试问题
Q: 测试覆盖率不足？
A: 使用 `pytest --cov-report=html` 生成详细报告分析

### 4. 工具问题
Q: pre-commit检查失败？
A: 运行 `pre-commit run --all-files` 手动检查所有文件

## 扩展阅读

- [Poetry文档](https://python-poetry.org/docs/)
- [MkDocs文档](https://www.mkdocs.org/)
- [pytest文档](https://docs.pytest.org/)
- [GitHub Actions文档](https://docs.github.com/actions) 