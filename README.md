# Python Project Template
# Python项目模板

一个具有企业级特性的完整Python项目模板。

## ✨ 特性

* 🐍 支持 Python 3.11+ (推荐 3.11.8)
* 📦 使用 Poetry 进行依赖管理
* 🚀 完整的代码质量检查工具链
  - Black (^24.2.0) - 代码格式化
  - Ruff (^0.3.0) - 快速代码分析
  - MyPy (^1.8.0) - 类型检查
  - Bandit (^1.7.7) - 安全检查
  - isort (^5.13.2) - 导入排序
* 📊 测试与覆盖率
  - pytest (^8.0.1)
  - pytest-cov (^4.1.0)
  - pytest-asyncio (^0.23.5)
* 📚 文档工具
  - Sphinx (^7.2.6)
  - sphinx-rtd-theme (^2.0.0)
* 🔄 Git 工作流集成
  - pre-commit (^3.6.2)
  - GitHub Actions CI/CD
* 🛠️ 核心依赖
  - pydantic (^2.6.3)
  - python-dotenv (^1.0.1)
  - structlog (^24.1.0)
  - sqlalchemy (^2.0.27)

## 🚀 快速开始

### 前置要求

* Python 3.11+ (推荐 3.11.8)
* Poetry
* Git

### 创建新项目

```bash
# 安装 cookiecutter
pip install cookiecutter

# 从模板创建项目
cookiecutter https://github.com/nighm/cookiecutter-python-template.git
```

### 项目设置

```bash
# 安装依赖
poetry install

# 设置 pre-commit 钩子
poetry run pre-commit install

# 运行测试
poetry run pytest
```

## 📁 项目结构

```
├── src/                    # 源代码目录
├── tests/                  # 测试文件
│   ├── quality_examples/   # 质量检查示例
│   └── ...
├── docs/                   # 文档
├── scripts/                # 工具脚本
├── config/                 # 配置文件
│   └── quality/           # 质量检查配置
├── .github/               # GitHub Actions 配置
├── pyproject.toml        # Poetry 项目配置
└── README.md            # 项目说明
```

## 🔍 代码质量检查

项目支持三个级别的代码质量检查：

* basic - 基础检查（格式化、类型检查）
* standard - 标准检查（包含安全检查、复杂度分析）
* advanced - 高级检查（包含更严格的规则和额外的检查）

运行检查：

```bash
poetry run python scripts/run_quality_checks.py --level [basic|standard|advanced]
```

## 📖 文档

* [快速入门指南](./docs/quick_start.md)
* [代码质量配置指南](./docs/code_quality_config.md)
* [质量检查示例](./docs/quality_examples.md)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件

## 👥 作者

* humingming (nighm@sina.com)

## 🙏 致谢

* 感谢所有贡献者
* 借鉴了现代 Python 最佳实践
* 使用了最新的开发工具和标准
