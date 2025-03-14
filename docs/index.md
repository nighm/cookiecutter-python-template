# Python项目模板使用指南

## 快速开始

### 前置条件
- Python 3.11+ (推荐3.11.x，目前已验证)
- Poetry 包管理工具
- Git (用于版本控制)

### 创建新项目
1. 创建工作目录:
   ```powershell
   # 在用户目录下创建 projects 文件夹（如果不存在）
   mkdir %USERPROFILE%\projects
   
   # 切换到 projects 目录
   cd %USERPROFILE%\projects
   ```

2. 安装 cookiecutter:
   ```bash
   pip install cookiecutter
   ```

3. 使用模板创建项目:
   ```bash
   cookiecutter https://github.com/your-username/cookiecutter-python-template.git
   ```

4. 按提示填写项目信息:
   - project_name: 项目名称
   - project_slug: 项目标识符(用作包名)
   - project_description: 项目描述
   - author_name: 作者姓名
   - author_email: 作者邮箱

5. 初始化项目:
   ```bash
   cd your-project-name
   poetry install
   poetry shell
   pre-commit install
   ```

## 项目结构

```
your-project-name/
├── src/
│   └── your_package/
│       ├── __init__.py
│       └── core/
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── docs/
│   └── *.md
├── scripts/
│   └── run_quality_checks.py
├── .env.example
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

## 代码质量工具

本模板集成了三个层次的代码质量检查工具：

### 基础层
- **black**: 代码格式化
- **isort**: 导入语句排序
- **ruff**: 快速代码检查
- **mypy**: 类型检查
- **pydocstyle**: 文档风格检查
- **pytest**: 单元测试

### 标准层
- **pytest-cov**: 测试覆盖率
- **pylint**: 深度代码分析
- **bandit**: 安全检查
- **vulture**: 死代码检测

### 高级层
- **safety**: 依赖安全检查
- **xenon**: 代码复杂度检查
- **radon**: 代码度量

## 常用命令

### 开发相关
```bash
# 安装依赖
poetry install

# 激活虚拟环境
poetry shell

# 运行测试
pytest

# 运行带覆盖率的测试
pytest --cov=src

# 运行代码质量检查
python scripts/run_quality_checks.py
```

### 文档相关
```bash
# 构建文档
mkdocs build

# 本地预览文档
mkdocs serve
```

## 最佳实践

### 1. 代码组织
- 使用 `src` 布局组织源代码
- 测试文件与源文件保持相同的结构
- 使用 `__init__.py` 定义公共API

### 2. 依赖管理
- 使用 `poetry add` 添加新依赖
- 使用 `poetry add -D` 添加开发依赖
- 定期更新依赖 `poetry update`

### 3. 版本控制
- 遵循语义化版本规范
- 使用 pre-commit hooks 保证代码质量
- 保持 CHANGELOG.md 更新

### 4. 测试规范
- 编写单元测试覆盖核心功能
- 使用 pytest fixtures 复用测试代码
- 保持测试简单、独立、可重复

## 常见问题

### Q: 如何添加新的依赖？
A: 使用 `poetry add package_name` 添加依赖，或手动编辑 `pyproject.toml` 后运行 `poetry install`。

### Q: 如何运行特定的测试？
A: 使用 `pytest tests/test_specific.py -v` 运行特定测试文件，或 `pytest -k "test_name"` 运行特定测试函数。

### Q: 如何处理代码质量工具的错误？
A: 
1. 先运行 `black` 和 `isort` 修复格式问题
2. 使用 `ruff` 检查并修复基本问题
3. 根据 `mypy` 提示修复类型问题
4. 最后处理 `pylint` 的警告

## 更新日志
详见 [CHANGELOG.md](../CHANGELOG.md)