# 更新日志

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2025-03-11

### ✨ 新增
- 初始版本发布
- 支持 Python 3.11+ (推荐 3.11.8)
- 集成最新版本的代码质量工具：
  - Black (^24.2.0)
  - Ruff (^0.3.0)
  - MyPy (^1.8.0)
  - Bandit (^1.7.7)
  - isort (^5.13.2)
- 添加测试框架支持：
  - pytest (^8.0.1)
  - pytest-cov (^4.1.0)
  - pytest-asyncio (^0.23.5)
- 添加文档工具：
  - Sphinx (^7.2.6)
  - sphinx-rtd-theme (^2.0.0)
- 集成核心依赖：
  - pydantic (^2.6.3)
  - python-dotenv (^1.0.1)
  - structlog (^24.1.0)
  - sqlalchemy (^2.0.27)

### 🔧 优化
- 移除了对 Python 3.11 以下版本的支持
- 移除了 pytype 和 scalene 工具（兼容性问题）
- 优化了代码质量检查的配置
- 改进了项目文档结构

### 🐛 修复
- 修复了 pre-commit 配置问题
- 修复了 isort 配置中缺少的参数
- 修复了部分文件的格式化问题

### 📝 文档
- 更新了 README.md，使用更清晰的结构
- 添加了详细的代码质量配置说明
- 添加了质量检查示例 