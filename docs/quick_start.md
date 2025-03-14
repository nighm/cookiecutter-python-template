# 快速入门指南

## 1. 环境准备

### 1.1 Python环境
确保你的系统已安装Python 3.11或更高版本：
```bash
python --version  # 应该显示 3.11.x
```

### 1.2 安装必要工具
```bash
# 安装 poetry（包管理工具）
curl -sSL https://install.python-poetry.org | python3 -

# 安装 cookiecutter（项目模板工具）
pip install cookiecutter

# 验证安装
poetry --version
cookiecutter --version
```

## 2. 创建新项目

### 2.1 使用模板创建项目
```bash
cookiecutter https://github.com/your-username/cookiecutter-python-template.git
```

### 2.2 填写项目信息
在交互式提示中填写以下信息：
- `project_name`: 项目名称（例如：My Amazing Project）
- `project_slug`: 项目标识符（例如：my_amazing_project）
- `project_description`: 项目描述
- `author_name`: 你的名字
- `author_email`: 你的邮箱

### 2.3 初始化项目
```bash
# 进入项目目录
cd my_amazing_project

# 初始化 git 仓库
git init

# 安装依赖
poetry install

# 激活虚拟环境
poetry shell

# 安装 pre-commit hooks
pre-commit install
```

## 3. 项目开发

### 3.1 项目结构
```
my_amazing_project/
├── src/
│   └── my_amazing_project/
│       ├── __init__.py
│       └── core/
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── docs/
│   └── *.md
└── scripts/
    └── run_quality_checks.py
```

### 3.2 开发流程
1. 在 `src/my_amazing_project/` 下创建你的代码
2. 在 `tests/` 下编写对应的测试
3. 运行测试和代码质量检查：
   ```bash
   # 运行测试
   pytest
   
   # 运行代码质量检查
   python scripts/run_quality_checks.py
   ```

### 3.3 文档编写
1. 在 `docs/` 目录下编写文档
2. 本地预览文档：
   ```bash
   mkdocs serve
   ```
3. 构建文档：
   ```bash
   mkdocs build
   ```

## 4. 代码质量保证

### 4.1 自动格式化
```bash
# 格式化代码
black .

# 排序导入
isort .
```

### 4.2 代码检查
```bash
# 运行类型检查
mypy src tests

# 运行代码分析
ruff check .

# 运行安全检查
bandit -r src
```

### 4.3 测试覆盖率
```bash
pytest --cov=src --cov-report=html
```

## 5. 依赖管理

### 5.1 添加依赖
```bash
# 添加生产依赖
poetry add package_name

# 添加开发依赖
poetry add -D package_name
```

### 5.2 更新依赖
```bash
# 更新所有依赖
poetry update

# 更新特定依赖
poetry update package_name
```

## 6. 版本发布

### 6.1 版本管理
```bash
# 更新版本号
poetry version patch  # 或 minor 或 major

# 构建项目
poetry build
```

### 6.2 发布检查清单
1. 更新 CHANGELOG.md
2. 运行完整的测试套件
3. 运行所有代码质量检查
4. 更新文档
5. 创建发布标签

## 7. 常见问题

### Q: 如何运行特定的测试？
```bash
pytest tests/test_specific.py -v
pytest -k "test_name"
```

### Q: 如何查看代码覆盖率报告？
```bash
# 生成覆盖率报告
pytest --cov=src --cov-report=html
# 打开 htmlcov/index.html 查看报告
```

### Q: 如何处理依赖冲突？
1. 查看详细依赖树：
   ```bash
   poetry show --tree
   ```
2. 更新特定包：
   ```bash
   poetry update package_name
   ```
3. 手动编辑 `pyproject.toml` 调整版本约束

### Q: pre-commit hooks 太慢怎么办？
1. 只对修改的文件运行检查：
   ```bash
   git add .
   pre-commit run --files $(git diff --cached --name-only)
   ```
2. 使用缓存：
   ```bash
   pre-commit run --all-files  # 首次运行会建立缓存
   ```

## 8. 下一步

- 阅读[代码质量工具指南](code_quality_tools.md)了解更多细节
- 查看[项目配置指南](project_details.md)了解更多配置选项
- 参考[示例代码](quality_examples.md)学习最佳实践 