# Python 项目模板学习指南

本指南将帮助你逐步掌握这个项目模板的所有功能。我们将按照由浅入深的顺序进行学习。

## 目录

1. [基础环境设置](#1-基础环境设置)
2. [项目创建和结构](#2-项目创建和结构)
3. [代码质量工具](#3-代码质量工具)
4. [测试框架](#4-测试框架)
5. [文档系统](#5-文档系统)
6. [CI/CD 和 Git 工作流](#6-cicd-和-git-工作流)
7. [依赖管理](#7-依赖管理)
8. [最佳实践](#8-最佳实践)

## 1. 基础环境设置

### 1.1 Python 环境
```bash
# 检查 Python 版本（需要 3.11+，推荐 3.11.8）
python --version

# 如果需要，安装 pyenv 来管理 Python 版本
# Windows:
pip install pyenv-win
# Linux/MacOS:
curl https://pyenv.run | bash

# 安装并设置 Python 3.11.8
pyenv install 3.11.8
pyenv global 3.11.8
```

### 1.2 必要工具安装
```bash
# 安装项目创建工具
pip install cookiecutter

# 安装依赖管理工具
pip install poetry

# 验证安装
cookiecutter --version
poetry --version
```

## 2. 项目创建和结构

### 2.1 创建新项目
```bash
# 克隆并创建项目
cookiecutter https://github.com/nighm/cookiecutter-python-template

# 按提示填写项目信息：
# - project_name: 你的项目名称
# - project_slug: 项目目录名（自动生成）
# - python_version: 选择 Python 版本
# - 其他选项可保持默认
```

### 2.2 项目结构说明
```
项目根目录/
├── src/                    # 源代码目录
│   └── your_project/      # 主要代码
├── tests/                 # 测试文件
│   ├── unit/             # 单元测试
│   └── integration/      # 集成测试
├── docs/                 # 文档目录
├── scripts/              # 工具脚本
└── config/              # 配置文件
```

## 3. 代码质量工具

### 3.1 代码格式化
```bash
# 使用 Black 格式化代码
poetry run black .

# 使用 isort 排序导入
poetry run isort .
```

### 3.2 代码分析
```bash
# 使用 Ruff 进行快速代码分析
poetry run ruff check .

# 使用 MyPy 进行类型检查
poetry run mypy src

# 使用 Bandit 进行安全检查
poetry run bandit -r src
```

### 3.3 综合质量检查
```bash
# 基础级别检查（日常开发使用）
poetry run python scripts/run_quality_checks.py --level basic

# 标准级别检查（提交代码前使用）
poetry run python scripts/run_quality_checks.py --level standard

# 高级级别检查（发布前使用）
poetry run python scripts/run_quality_checks.py --level advanced
```

## 4. 测试框架

### 4.1 编写测试
```python
# tests/test_example.py
def test_feature():
    assert True

# 异步测试
import pytest
@pytest.mark.asyncio
async def test_async_feature():
    assert True
```

### 4.2 运行测试
```bash
# 运行所有测试
poetry run pytest

# 运行带覆盖率报告的测试
poetry run pytest --cov

# 生成 HTML 覆盖率报告
poetry run pytest --cov --cov-report=html
```

## 5. 文档系统

### 5.1 文档结构
```
docs/
├── index.md          # 文档首页
├── quick_start.md    # 快速入门
├── api/              # API 文档
└── guides/           # 使用指南
```

### 5.2 构建文档
```bash
# 安装文档工具
poetry install

# 构建文档
cd docs
poetry run make html
```

## 6. CI/CD 和 Git 工作流

### 6.1 Git 提交规范
```bash
# 设置 pre-commit 钩子
poetry run pre-commit install

# 提交示例
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update documentation"
```

### 6.2 GitHub Actions
- 推送代码自动触发测试
- PR 自动运行代码质量检查
- 发布自动构建文档

## 7. 依赖管理

### 7.1 管理项目依赖
```bash
# 添加生产依赖
poetry add package_name

# 添加开发依赖
poetry add --dev package_name

# 更新依赖
poetry update

# 查看依赖树
poetry show --tree
```

### 7.2 虚拟环境
```bash
# 激活虚拟环境
poetry shell

# 退出虚拟环境
exit
```

## 8. 最佳实践

### 8.1 开发流程
1. 激活虚拟环境：`poetry shell`
2. 编写代码和测试
3. 运行基础质量检查：`python scripts/run_quality_checks.py --level basic`
4. 运行测试：`pytest`
5. 提交代码：`git commit`
6. 推送前运行完整检查：`python scripts/run_quality_checks.py --level standard`

### 8.2 发布流程
1. 更新版本号：`poetry version patch/minor/major`
2. 更新 CHANGELOG.md
3. 运行高级质量检查：`python scripts/run_quality_checks.py --level advanced`
4. 提交更改
5. 创建发布标签：`git tag v1.0.0`
6. 推送：`git push && git push --tags`

### 8.3 文档维护
- 及时更新 API 文档
- 添加使用示例
- 更新版本说明
- 维护 CHANGELOG.md 