# Python项目模板

一个现代化的Python项目模板，提供完整的项目结构和最佳实践指南。

## 特性

- 标准化的项目结构
- 国际化支持 (i18n)
- 自动生成的文档 (Sphinx)
- 完整的测试框架
- 监控和指标收集
- 异步支持
- Docker支持
- CI/CD配置

## 快速开始

### 使用此模板

1. 点击GitHub的"Use this template"按钮创建新项目
2. 克隆你的新项目
```bash
git clone <your-project-url>
cd <your-project-name>
```

3. 安装依赖
```bash
# 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install
```

4. 初始化项目
```bash
# 安装pre-commit钩子
poetry run pre-commit install

# 运行测试确保一切正常
poetry run pytest
```

### 项目结构

```
.
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   ├── utils/             # 通用工具
│   └── config/            # 配置文件
├── tests/                 # 测试目录
│   ├── unit/             # 单元测试
│   ├── integration/      # 集成测试
│   └── performance/      # 性能测试
├── docs/                  # 文档
│   ├── en/               # 英文文档
│   └── zh/               # 中文文档
├── examples/             # 示例代码
├── scripts/              # 工具脚本
└── resources/            # 资源文件
```

## 开发指南

### 配置开发环境

1. 创建配置文件
```bash
cp .env.example .env
```

2. 修改配置
编辑 `.env` 文件，设置必要的环境变量。

### 运行测试

```bash
# 运行所有测试
poetry run pytest

# 运行特定测试
poetry run pytest tests/unit/

# 生成覆盖率报告
poetry run pytest --cov=src
```

### 代码质量

```bash
# 格式化代码
poetry run black src tests

# 类型检查
poetry run mypy src

# 代码风格检查
poetry run flake8 src
```

### 生成文档

```bash
# 生成英文文档
cd docs/en && poetry run make html

# 生成中文文档
cd docs/zh && poetry run make html
```

## 如何运行应用

1. 确保已安装依赖：
   ```bash
   poetry install
   ```
2. 运行应用：
   ```bash
   poetry run python -m src
   ```
3. 访问应用：
   - 如果是Web应用，打开浏览器并访问`http://localhost:8000`（或其他指定端口）。

## 项目定制

### 1. 修改项目信息

更新以下文件中的项目信息：
- `pyproject.toml`：项目名称、版本等
- `docs/conf.py`：文档信息
- `README.md`：项目描述

### 2. 选择需要的组件

本模板提供多个可选组件：
- 数据库支持 (SQLAlchemy)
- 缓存支持 (Redis)
- 任务队列 (Celery)
- API服务 (FastAPI)
- CLI工具 (Click)

根据需要保留或删除相关代码。

### 3. 配置CI/CD

根据你的需求修改 `.github/workflows/` 中的工作流配置。

## 最佳实践

- 使用 Poetry 管理依赖
- 编写详细的文档字符串
- 添加类型注解
- 保持较高的测试覆盖率
- 使用异步编程处理I/O操作
- 实现健康检查和监控
- **错误处理**：确保在代码中添加适当的错误处理逻辑，使用try-except语句捕获异常，并记录错误信息。
- **日志记录**：使用`structlog`或`logging`模块进行日志记录，以便在运行时跟踪应用程序的状态和错误。
- **错误处理和日志记录**：在代码中添加适当的错误处理逻辑和日志记录机制，以便在运行时跟踪应用程序的状态和错误。

## 常见问题

### 如何安装依赖？
使用以下命令安装项目的所有依赖：
```bash
poetry install
```

### 如何运行测试？
使用以下命令运行所有测试：
```bash
poetry run pytest
```

### 如何生成文档？
使用以下命令生成英文和中文文档：
```bash
cd docs/en && poetry run make html
cd docs/zh && poetry run make html
```

## 示例代码

```python
from src import your_module

# 示例功能
result = your_module.your_function()
print(result)

# 示例功能2
def add(a, b):
    return a + b

result = add(1, 2)
print(result)
```

## 许可证

MIT License

## 贡献指南

欢迎提交Issue和Pull Request！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多信息。
