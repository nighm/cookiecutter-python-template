# Python 项目模板使用指南

本文档展示了如何使用项目模板创建一个实际的 Python 项目。

## 1. 环境准备

### 1.1 工作目录设置

#### Windows 系统
```powershell
# 创建项目目录
cd ~
mkdir -p projects
cd projects
```

#### Linux/MacOS 系统
```bash
# 创建项目目录
cd ~
mkdir -p projects
cd projects
```

### 1.2 必要工具安装

在开始之前，请确保安装以下工具：

1. **Python 3.11**
2. **Poetry**（包管理工具）
3. **Cookiecutter**（项目模板工具）

#### Windows 系统
```powershell
# 1. 安装 Python 3.11
pyenv install 3.11.8
pyenv local 3.11.8

# 2. 安装 Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# 3. 安装 Cookiecutter
pip install cookiecutter
```

#### Linux/MacOS 系统
```bash
# 1. 安装 Python 3.11
pyenv install 3.11.8
pyenv local 3.11.8

# 2. 安装 Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 3. 安装 Cookiecutter
pip install cookiecutter
```

### 1.3 安装验证

运行以下命令验证安装：

```bash
# 验证 Python
python --version  # 应显示 3.11.8

# 验证 Poetry
poetry --version

# 验证 Cookiecutter
cookiecutter --version
```

## 2. 创建新项目

### 2.1 使用模板创建项目

在工作目录下执行：

```bash
cookiecutter https://github.com/nighm/cookiecutter-python-template.git
```

系统会提示您输入以下信息：
```
project_name [My Project]: 您的项目名称
project_slug [my_project]: 项目目录名
project_description [A Python project]: 项目描述
author_name [Your Name]: 作者姓名
author_email [your.email@example.com]: 电子邮件
python_version [3.11]: Python版本
use_docker [y]: 是否使用Docker
use_github_actions [y]: 是否使用GitHub Actions
```

> 💡 **提示**：如果想了解命令执行过程中各种输出的详细含义，请参考 [命令输出说明文档](command_output_explanation.md)。

### 2.2 项目初始化

在项目创建完成后，需要执行以下步骤来初始化项目：

#### 2.2.1 进入项目目录
```bash
cd <your_project_name>
```

#### 2.2.2 初始化依赖管理

首次使用时，建议配置国内镜像源以加快安装速度：
```bash
# 配置 pip 使用国内镜像源（推荐）
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
pip config set global.trusted-host mirrors.ustc.edu.cn

# 或者配置 Poetry 使用国内镜像源
poetry source add --priority=default aliyun https://mirrors.aliyun.com/pypi/simple/
```

安装项目依赖有两种方式：

1. 使用 Poetry 安装（推荐但可能遇到网络问题）：
```bash
# 生成 poetry.lock 文件
poetry lock

# 安装项目依赖
poetry install
```

2. 如果 Poetry 安装失败，可以使用 pip 安装（更稳定的替代方案）：
```bash
# 在项目目录下执行
pip install -e .
```

> 💡 **依赖安装说明**：
> - Poetry 在解析依赖时可能需要访问 pypi.org
> - 如果遇到网络问题，建议使用 pip 安装方式
> - 两种安装方式的效果是相同的
> - 安装完成后，可以使用 `pip list` 检查已安装的包
> - `poetry.lock` 文件用于锁定项目所有依赖的精确版本
> - 建议将 lock 文件提交到版本控制系统

#### 2.2.3 初始化开发环境

在开始开发之前，我们需要进行一系列的环境检查和初始化步骤：

1. 检查Python环境
```bash
# 检查Python版本
python --version

# 检查pip版本
pip --version

# 检查Poetry版本
poetry --version

# 检查当前Python解释器路径
where python
```

2. 检查虚拟环境状态
```bash
# 查看Poetry的虚拟环境列表
poetry env list

# 查看当前激活的虚拟环境
poetry env info

# 如果需要创建并激活虚拟环境（Poetry 1.x版本）
poetry shell

# 如果使用Poetry 2.0及以上版本
poetry env use python
poetry env info  # 确认环境已正确创建
poetry env activate  # 激活环境
```

3. 验证虚拟环境激活状态
```bash
# 检查当前Python解释器路径，应该指向虚拟环境
where python

# 检查pip安装位置，应该指向虚拟环境
pip -V

# 在PowerShell中，可以通过以下命令查看当前虚拟环境
$env:VIRTUAL_ENV
```

4. 安装项目包（开发模式）
```bash
# 确保在项目根目录下
pip install -e .

# 或使用poetry安装
poetry install
```

5. 安装pre-commit钩子
```bash
# 安装pre-commit钩子
poetry run pre-commit install

# 验证pre-commit安装
poetry run pre-commit --version
```

6. 常见问题排查：
- 如果找不到python_project_template模块：
  - 检查是否已在开发模式下安装项目：`pip list | findstr python-project-template`
  - 检查PYTHONPATH是否包含项目根目录
  - 检查项目是否有正确的setup.py或pyproject.toml

- 如果虚拟环境未正确激活：
  - 检查$env:VIRTUAL_ENV环境变量
  - 检查Python解释器路径
  - 尝试重新激活环境

- 如果依赖安装失败：
  - 检查网络连接
  - 验证pip源配置：`pip config list`
  - 检查poetry源配置：`poetry config --list`

#### 2.2.4 验证安装
```bash
# 运行测试确保环境正确配置
poetry run pytest

# 检查代码质量工具是否正常工作
poetry run pre-commit run --all-files
```

#### 2.2.5 故障排除

如果在初始化过程中遇到问题，可以参考以下解决方案：

- 依赖安装失败
  - 检查网络连接
  - 确保镜像源配置正确
  - 确保 Python 版本符合要求

- lock 文件生成失败
  ```bash
  # 尝试使用 --no-update 选项
  poetry lock --no-update
  ```

### 2.3 快速创建选项

1. **使用默认值创建**：
   ```bash
   cookiecutter https://github.com/nighm/cookiecutter-python-template.git --no-input
   ```

2. **使用特定版本**：
   ```bash
   cookiecutter https://github.com/nighm/cookiecutter-python-template.git --checkout v1.0.0
   ```

3. **离线创建**：
   ```bash
   # 克隆模板
   git clone https://github.com/nighm/cookiecutter-python-template.git
   # 使用本地模板
   cookiecutter ./cookiecutter-python-template
   ```

## 3. 项目结构

生成的项目结构如下：

```
项目根目录/
├── src/                 # 源代码目录
├── tests/              # 测试文件
├── docs/               # 项目文档
├── scripts/            # 工具脚本
├── config/             # 配置文件
│   └── quality/        # 代码质量检查配置
├── .github/            # GitHub 相关配置
├── .env               # 环境变量
└── pyproject.toml     # 项目配置文件
```

详细的目录说明请参考 [项目结构文档](project_structure.md)。

## 4. 项目配置

### 4.1 依赖安装

```bash
# 进入项目目录
cd 您的项目名称

# 安装依赖
poetry install
```

如果遇到网络问题，可以使用国内镜像：
```bash
# 配置镜像源
poetry config repositories.aliyun https://mirrors.aliyun.com/pypi/simple/

# 重新安装
poetry install
```

### 4.2 开发环境设置

```bash
# 安装 pre-commit hooks
poetry run pre-commit install

# 初始化虚拟环境
poetry shell
```

## 5. 开发工作流

### 5.1 代码质量检查

```bash
# 运行所有检查
poetry run pre-commit run --all-files

# 运行测试
poetry run pytest

# 检查代码覆盖率
poetry run pytest --cov=src
```

### 5.2 文档维护

```bash
# 构建文档
cd docs && poetry run make html

# 本地预览
poetry run python -m http.server --directory docs/_build/html 8000
```

## 6. 常见问题

### 6.1 依赖安装问题

如果 Poetry 安装依赖失败：
1. 检查网络连接
2. 使用国内镜像源
3. 尝试手动安装：
   ```bash
   pip install -r <(poetry export --dev)
   ```

### 6.2 代码检查问题

如果代码检查不通过：
1. 运行自动修复：
   ```bash
   poetry run black .
   poetry run ruff --fix .
   ```
2. 查看详细错误信息：
   ```bash
   poetry run mypy src
   ```

## 7. 更多资源

- [完整文档](https://项目文档地址)
- [问题反馈](https://github.com/用户名/项目名/issues)
- [更新日志](CHANGELOG.md)