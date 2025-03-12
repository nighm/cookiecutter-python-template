# Python项目模板快速入门指南

## 一、简介

这是一个现代化的 Python 项目模板，专注于代码质量和开发效率。模板使用 Poetry 进行依赖管理，支持 Python 3.11+ 版本，并集成了全面的代码质量检查工具。

## 二、快速开始

### 2.1 环境准备
```bash
# 1. 确保 Python 版本正确（推荐 3.11.8）
python --version

# 2. 安装必要工具
pip install cookiecutter poetry

# 3. 创建新项目
cookiecutter https://github.com/nighm/cookiecutter-python-template

# 4. 安装项目依赖
cd 你的项目名称
poetry install

# 5. 设置 pre-commit 钩子
poetry run pre-commit install
```

### 2.2 项目结构
```
你的项目/
├── src/                    # 源代码目录
├── tests/                  # 测试文件
│   ├── quality_examples/   # 质量检查示例
│   └── ...
├── docs/                   # 文档
├── scripts/                # 工具脚本
├── config/                 # 配置文件
│   └── quality/           # 质量检查配置
└── .github/               # GitHub Actions 配置
```

## 三、基本使用

### 3.1 开发流程
1. 激活环境：`poetry shell`
2. 编写代码：在 `src/` 目录下开发
3. 运行测试：`poetry run pytest`
4. 运行代码质量检查：`poetry run python scripts/run_quality_checks.py --level basic`

### 3.2 常用命令
```bash
# 运行测试（带覆盖率报告）
poetry run pytest

# 代码质量检查
poetry run python scripts/run_quality_checks.py --level [basic|standard|advanced]

# 格式化代码
poetry run black .
poetry run isort .

# 类型检查
poetry run mypy src

# 代码分析
poetry run ruff check .
```

## 四、文件说明

### 4.1 重要文件
- `pyproject.toml`: 项目配置和依赖管理
- `poetry.lock`: 依赖版本锁定
- `.pre-commit-config.yaml`: Git 提交钩子配置
- `.env`: 环境变量（从 .env.example 复制）

### 4.2 配置文件
- `config/quality/basic/`: 基础级别质量检查配置
- `config/quality/standard/`: 标准级别质量检查配置
- `config/quality/advanced/`: 高级级别质量检查配置

## 五、代码质量工具

### 5.1 已集成的工具
- Black (^24.2.0): 代码格式化
- Ruff (^0.3.0): 快速代码分析
- MyPy (^1.8.0): 类型检查
- Bandit (^1.7.7): 安全检查
- isort (^5.13.2): 导入排序

### 5.2 运行质量检查
```bash
# 基础检查（推荐日常使用）
poetry run python scripts/run_quality_checks.py --level basic

# 完整检查（推荐提交前运行）
poetry run python scripts/run_quality_checks.py --level standard
```

## 六、常见问题

### 6.1 "如何添加新依赖？"
```bash
# 添加主依赖
poetry add 包名

# 添加开发依赖
poetry add --dev 包名
```

### 6.2 "如何更新依赖？"
```bash
# 更新所有依赖
poetry update

# 更新特定依赖
poetry update 包名
```

## 七、下一步

- 查看 [代码质量配置指南](./code_quality_config.md) 了解更多配置选项
- 查看 [质量检查示例](./quality_examples.md) 了解各级别检查的区别
- 参考 `tests/quality_examples/` 目录下的示例代码 