# Python项目模板

一个注重代码质量和开发效率的现代化Python项目模板。

## ✨ 特性

- 📦 使用Poetry进行依赖管理和打包
- 🔍 集成全面的代码质量检查工具链
- 📝 自动API文档生成和项目文档
- 🚀 GitHub Actions持续集成/持续部署
- 🧪 完整的测试框架和覆盖率报告
- 🔒 安全检查和依赖审计
- 🐳 Docker支持（可选）

## 🚀 快速开始

### 环境要求

- Python 3.11+ 
- Poetry
- Git

### 创建项目

```bash
# 安装cookiecutter
pip install cookiecutter

# 创建项目
cookiecutter https://github.com/your-username/cookiecutter-python-template.git

# 初始化
cd your-project-name
poetry install
poetry shell
pre-commit install
```

## 📚 文档

- [快速入门指南](docs/quick_start.md) - 详细的项目创建和初始化步骤
- [项目详细说明](docs/project_details.md) - 项目结构和配置说明
- [开发指南](docs/development_guide.md) - 开发流程和最佳实践
- [代码质量](docs/code_quality.md) - 代码质量工具和规范

## 🛠️ 主要命令

```bash
# 开发
poetry install        # 安装依赖
poetry shell         # 激活环境
pytest               # 运行测试
pytest --cov=src     # 测试覆盖率报告

# 代码质量
python scripts/run_quality_checks.py  # 运行所有质量检查
black .              # 格式化代码
isort .             # 整理导入

# 文档
mkdocs serve        # 本地预览文档
mkdocs build        # 构建文档
```

## 📂 项目结构

```
your-project-name/
├── src/                    # 源代码
├── tests/                  # 测试文件
├── docs/                   # 文档
├── scripts/                # 工具脚本
└── [配置文件]
```

## 🤝 贡献

欢迎贡献！请查看[贡献指南](CONTRIBUTING.md)了解详情。

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 📋 更新日志

查看[CHANGELOG.md](CHANGELOG.md)了解版本更新历史。
