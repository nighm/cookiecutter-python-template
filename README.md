# Python Project Template
# Python项目模板

A comprehensive Python project template with enterprise-grade features.
一个具有企业级特性的完整Python项目模板。

## Features | 特性

- ✨ Modern Python project structure | 现代化的Python项目结构
- 🚀 CI/CD with GitHub Actions | 使用GitHub Actions的CI/CD流程
- 📊 Multi-level code quality checks | 多级别代码质量检查
- 📚 Comprehensive documentation | 完整的文档体系
- 🔧 Development tools integration | 开发工具集成
- 🐳 Docker support | Docker支持
- 🔄 Version management | 版本管理
- 🌍 Internationalization ready | 国际化支持

## Quick Start | 快速开始

### Prerequisites | 前置要求

- Python 3.8+ | Python 3.8或更高版本
- Poetry | Poetry包管理工具
- Git | Git版本控制

### Installation | 安装

```bash
# Install cookiecutter | 安装cookiecutter
pip install cookiecutter

# Create project from template | 从模板创建项目
cookiecutter https://github.com/nighm/cookiecutter-python-template.git
```

### Development | 开发

```bash
# Install dependencies | 安装依赖
poetry install

# Setup pre-commit hooks | 设置pre-commit钩子
poetry run pre-commit install

# Run tests | 运行测试
poetry run pytest
```

## Project Structure | 项目结构

```
├── src/                    # Source code | 源代码
├── tests/                  # Test files | 测试文件
├── docs/                   # Documentation | 文档
├── .github/               # GitHub configuration | GitHub配置
├── pyproject.toml         # Project configuration | 项目配置
└── README.md             # Project readme | 项目说明
```

## Documentation | 文档

- [Quick Start Guide | 快速入门指南](docs/quick_start.md)
- [Detailed Documentation | 详细文档](docs/detailed.md)
- [Code Quality Guide | 代码质量指南](docs/code_quality.md)

## Contributing | 贡献指南

Contributions are welcome! Please feel free to submit a Pull Request.
欢迎贡献！请随时提交Pull Request。

## License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## Author | 作者

- humingming (nighm@sina.com)

## Acknowledgments | 致谢

- Thanks to all contributors | 感谢所有贡献者
- Inspired by modern Python best practices | 借鉴了现代Python最佳实践
