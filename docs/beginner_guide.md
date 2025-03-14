# Python 项目模板使用指南

## 目录
1. [快速开始](#快速开始)
2. [环境准备](#环境准备)
3. [获取项目模板](#获取项目模板)
4. [创建新项目](#创建新项目)
5. [项目开发指南](#项目开发指南)
6. [故障排除](#故障排除)

## 快速开始

如果你已经有了正确的 Python 环境（3.11.x），只需三步即可创建项目：

```bash
# 1. 安装 cookiecutter
pip install cookiecutter

# 2. 创建并切换到项目目录
# 在用户目录下创建 projects 文件夹（如果不存在）
mkdir %USERPROFILE%\projects

# 切换到 projects 目录
cd %USERPROFILE%\projects

# 3. 从 GitHub 创建项目（使用默认配置）
cookiecutter gh:nighm/cookiecutter-python-template --no-input
```

## 环境准备

### 1. Python 环境
1. 安装 Python 3.11.8：
   - 访问：https://www.python.org/downloads/
   - 下载 Python 3.11.8
   - 安装时勾选 "Add Python to PATH"

2. 验证安装：
   ```bash
   python --version
   # 应显示: Python 3.11.8
   ```

### 2. 开发工具
1. 安装 cookiecutter：
   ```bash
   pip install cookiecutter
   ```

2. 安装 Poetry：
   ```bash
   # Windows PowerShell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

   # 配置（推荐）
   poetry config virtualenvs.in-project true
   ```

## 获取项目模板

你可以通过以下三种方式之一获取模板：

### 方式一：直接从 GitHub 使用（推荐）
- 无需下载，直接创建项目
- 总是使用最新版本
- 需要网络连接

```bash
cookiecutter gh:nighm/cookiecutter-python-template
```

### 方式二：克隆仓库（适合二次开发）
- 完整的版本历史
- 可以修改模板
- 可以贡献代码

```bash
git clone https://github.com/nighm/cookiecutter-python-template.git
```

### 方式三：下载 ZIP（离线使用）
1. 访问：https://github.com/nighm/cookiecutter-python-template
2. 点击 "Code" -> "Download ZIP"
3. 解压到本地目录

## 创建新项目

### 1. 准备工作目录
```bash
# 创建并进入项目目录
mkdir D:\my_projects
cd D:\my_projects
```

### 2. 创建项目
1. 使用默认配置（快速）：
   ```bash
   cookiecutter gh:nighm/cookiecutter-python-template --no-input
   ```

2. 或自定义配置（推荐）：
   ```bash
   cookiecutter gh:nighm/cookiecutter-python-template
   ```
   根据提示填写：
   - project_name：项目名称
   - project_slug：项目标识符
   - project_description：项目描述
   - full_name：作者姓名
   - email：邮箱地址
   - version：版本号

### 3. 初始化项目
```bash
# 进入项目目录
cd your_project_name

# 安装依赖
poetry install

# 初始化 Git
git init
git add .
git commit -m "Initial commit"
```

## 项目开发指南

### 1. 项目结构
```
your_project_name/
├── src/                    # 源代码目录
├── tests/                  # 测试文件目录
├── docs/                   # 文档目录
├── .github/                # GitHub 配置
├── pyproject.toml         # 项目配置文件
└── README.md              # 项目说明文件
```

### 2. 依赖管理（v0.2.0）
本模板使用 Poetry 管理依赖，主要包括：

1. 核心依赖：
   - Python >= 3.11.0, < 3.12.0
   - pydantic >= 2.6.3（数据验证）
   - python-dotenv >= 1.0.1（环境变量）
   - structlog >= 24.1.0（日志）
   - sqlalchemy >= 2.0.27（ORM）

2. 开发工具：
   - black >= 24.2.0（格式化）
   - isort >= 5.13.2（导入排序）
   - ruff >= 0.3.0（代码分析）
   - mypy >= 1.8.0（类型检查）
   - bandit >= 1.7.7（安全检查）

3. 测试工具：
   - pytest >= 8.0.1
   - pytest-cov >= 4.1.0
   - pytest-asyncio >= 0.23.5

### 3. 开发流程
1. 激活环境：
   ```bash
   poetry shell
   ```

2. 安装依赖：
   ```bash
   poetry add package_name
   ```

3. 运行测试：
   ```bash
   poetry run pytest
   ```

4. 代码质量检查：
   ```bash
   poetry run black .
   poetry run isort .
   poetry run ruff check .
   poetry run mypy .
   ```

## 故障排除

### 1. 项目创建问题
1. Git 错误：
   ```
   FatalError: git failed
   ```
   解决：
   - 安装 Git
   - 添加到 PATH
   - 重启终端

2. pre-commit 错误：
   ```
   Failed to set up Poetry environment
   ```
   解决：
   - 可以忽略此错误
   - 项目创建后手动运行：
     ```bash
     poetry run pre-commit install
     ```

### 2. 依赖安装问题
1. Poetry 安装失败：
   - 使用管理员权限
   - 使用国内镜像：
     ```bash
     poetry config repositories.tuna https://pypi.tuna.tsinghua.edu.cn/simple
     ```

2. 包下载超时：
   - 设置更长的超时时间：
     ```bash
     poetry config installer.timeout 300
     ```

### 3. 环境问题
1. Python 版本不匹配：
   - 安装正确版本的 Python
   - 或修改 pyproject.toml 中的版本要求

2. 虚拟环境问题：
   ```bash
   # 重置虚拟环境
   rm -rf .venv
   poetry install
   ```

需要了解更多信息或遇到其他问题，请访问：
- 文档：https://github.com/nighm/cookiecutter-python-template/docs
- 问题反馈：https://github.com/nighm/cookiecutter-python-template/issues