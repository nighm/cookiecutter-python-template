# Python 项目模板使用指南

本指南将帮助你使用项目模板创建一个新的 Python 项目。每个步骤都会详细解释：
- 要做什么
- 为什么要这样做
- 具体怎么做
- 预期会看到什么结果
- 如果出错了怎么解决

## 准备工作：获取项目模板

在开始之前，你需要先获取项目模板。有两种方式：

### 方式一：从 GitHub 获取（推荐）

1. 使用 git clone 命令：
   ```bash
   # 切换到要存放模板的目录（这里用 D:\data\work 为例）
   cd D:\data\work
   
   # 从 GitHub 克隆项目模板
   git clone https://github.com/nighm/cookiecutter-python-template.git
   
   # 这个命令会：
   # 1. 在当前目录下创建 cookiecutter-python-template 文件夹
   # 2. 下载所有模板文件到这个文件夹中
   # 3. 自动设置好 Git 配置
   
   # ❌ 如果克隆失败，可能是因为：
   # 1. 网络连接问题 -> 检查网络或使用代理
   # 2. Git 未安装 -> 从 https://git-scm.com/downloads 下载安装
   # 3. 仓库地址错误 -> 检查地址是否正确
   ```

2. 或者直接下载 ZIP 文件：
   ```bash
   # 1. 访问项目地址：
   https://github.com/nighm/cookiecutter-python-template
   
   # 2. 点击绿色的 "Code" 按钮
   # 3. 选择 "Download ZIP"
   # 4. 解压下载的文件到 D:\data\work\cookiecutter-python-template
   
   # ⚠️ 注意：
   # - 这种方式不会包含 Git 历史记录
   # - 如果之后要贡献代码会比较麻烦
   # - 建议仅在无法使用 git clone 时使用此方式
   ```

### 方式二：使用本地模板

如果已经有人给你准备好了模板文件：

1. 确认模板位置：
   ```bash
   # 模板通常在这个位置：
   D:\data\work\cookiecutter-python-template
   
   # 确认文件夹存在
   dir D:\data\work\cookiecutter-python-template
   
   # 应该能看到这些关键文件：
   # - cookiecutter.json
   # - {{cookiecutter.project_slug}}/
   # - pyproject.toml
   ```

2. 验证模板完整性：
   ```bash
   # 检查必要的文件和目录是否存在
   cd D:\data\work\cookiecutter-python-template
   
   # 列出所有文件
   dir /s
   
   # 确保包含：
   # 1. cookiecutter.json（模板配置文件）
   # 2. {{cookiecutter.project_slug}}/ （项目模板目录）
   # 3. pyproject.toml（项目依赖配置）
   # 4. docs/（文档目录）
   # 5. tests/（测试目录）
   ```

### 为什么需要这些文件？

1. `cookiecutter.json`：
   - 定义项目创建时需要填写的信息
   - 设置默认值
   - 控制模板的行为

2. `{{cookiecutter.project_slug}}/`：
   - 实际的项目模板
   - 包含所有将被复制到新项目的文件
   - 文件名中的变量会被替换

3. `pyproject.toml`：
   - 定义项目的 Python 依赖
   - 指定项目的配置信息
   - 设置开发工具的配置

### 验证模板是否可用

在使用模板之前，可以先验证它是否可用：

```bash
# 1. 确保在正确的目录
cd D:\data\work

# 2. 尝试创建一个测试项目
cookiecutter cookiecutter-python-template --no-input

# 这个命令会：
# - 使用所有默认值创建项目
# - 如果成功，说明模板是可用的
# - 如果失败，会显示错误信息

# 3. 如果测试成功，可以删除测试项目
rm -r my-python-project  # 默认项目名

# ⚠️ 如果看到警告或错误：
# 1. 如果看到 "git failed" 错误：
#    - 确保已安装 Git：https://git-scm.com/downloads
#    - 确保 Git 已添加到系统环境变量
#    - 重新打开 PowerShell 后重试
#
# 2. 如果看到 "pre-commit" 相关错误：
#    - 这是正常的，不影响项目创建
#    - 可以在项目创建后手动运行：poetry run pre-commit install
#
# 3. 如果项目创建失败：
#    - 检查是否有足够的磁盘空间
#    - 确保有写入权限
#    - 尝试使用管理员权限运行 PowerShell
```

## 第一部分：使用模板创建项目

### 步骤 1：确认环境

1. 打开 PowerShell
   - 按 `Win + X`
   - 选择 "Windows PowerShell" 或 "Windows Terminal"
   - ⚠️ 建议：选择 "以管理员身份运行"

2. 确认你在项目模板目录下：
   ```bash
   # 查看当前目录
   pwd
   
   # 你应该看到类似这样的输出：
   Path
   ----
   D:\data\work\cookiecutter-python-template
   
   # ❌ 如果不是这个目录，使用以下命令切换：
   cd D:\data\work\cookiecutter-python-template
   
   # ⚠️ 重要：确保这个目录是你的项目模板目录
   # 如果切换失败，请检查：
   # 1. 目录是否存在
   # 2. 路径是否正确（注意大小写）
   # 3. 是否有权限访问该目录
   ```

3. 检查目录内容：
   ```bash
   # 查看目录中的文件
   dir
   
   # 你应该能看到这些关键文件和目录：
   Mode                 LastWriteTime         Length Name
   ----                 -------------         ------ ----
   d----               ...                          {{cookiecutter.project_slug}}/  # 模板目录
   -a---               ...                          cookiecutter.json              # 模板配置文件
   -a---               ...                          pyproject.toml                # Poetry 项目配置
   -a---               ...                          README.md                     # 项目说明文件
   
   # ❌ 如果看不到这些文件，特别是 cookiecutter.json 和模板目录，说明：
   # 1. 可能在错误的目录下
   # 2. 或模板文件不完整，需要重新获取模板
   ```

4. 检查 Python 版本：
   ```bash
   # 检查 Python 版本
   python --version
   
   # ✅ 应该看到：
   Python 3.11.8
   
   # ❌ 如果看到其他版本：
   # 1. 如果是 Python 2.x：必须升级
   # 2. 如果是 Python 3.x 但不是 3.11.8：
   #    - 建议安装 3.11.8
   #    - 或修改 pyproject.toml 中的 python 版本要求
   
   # ❌ 如果提示 'python' 不是内部或外部命令：
   # 1. 访问：https://www.python.org/downloads/
   # 2. 下载并安装 Python 3.11.8
   # 3. 安装时必须勾选"Add Python to PATH"
   # 4. 安装后需要重新打开 PowerShell
   ```

### 步骤 2：准备工作目录

1. 创建并进入工作目录：
   ```bash
   # 切换到要存放项目的驱动器（这里用 D 盘为例）
   cd D:\
   
   # 创建项目目录（如果已存在会提示，可以忽略）
   mkdir my_projects
   
   # 进入项目目录
   cd my_projects
   
   # 确认位置
   pwd
   
   # 应该看到：
   Path
   ----
   D:\my_projects
   ```

### 步骤 3：安装必要工具

1. 安装 cookiecutter：
   ```bash
   # 安装 cookiecutter 工具
   pip install cookiecutter
   
   # 这个命令会：
   # 1. 将 cookiecutter 安装到 Python 的包目录中
   #    - Windows: C:\Users\用户名\AppData\Local\Programs\Python\Python311\Lib\site-packages
   #    - 或者如果使用 pyenv: C:\Users\用户名\.pyenv\pyenv-win\versions\3.11.8\Lib\site-packages
   # 2. 将可执行文件放在 Python 的 Scripts 目录中
   #    - Windows: C:\Users\用户名\AppData\Local\Programs\Python\Python311\Scripts
   #    - 或者如果使用 pyenv: C:\Users\用户名\.pyenv\pyenv-win\versions\3.11.8\Scripts
   
   # 验证安装是否成功
   cookiecutter --version
   
   # 这个命令会显示：
   # - cookiecutter 的版本号
   # - 安装位置
   # - 使用的 Python 版本
   ```

2. 确认 Poetry 已安装：
   ```bash
   # 检查 Poetry 是否已安装及其版本
   poetry --version
   
   # 这个命令会：
   # - 显示已安装的 Poetry 版本
   # - Poetry 默认安装在：C:\Users\用户名\AppData\Roaming\Python\Scripts
   # - 配置文件位置：C:\Users\用户名\AppData\Roaming\pypoetry
   
   # ❌ 如果未安装，使用官方安装脚本安装：
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   
   # 这个安装命令会：
   # 1. 下载 Poetry 的安装脚本
   # 2. 将 Poetry 安装到用户目录，而不是系统目录
   # 3. 添加必要的环境变量
   ```

3. 配置 Poetry：
   ```bash
   # 设置虚拟环境在项目目录中创建
   poetry config virtualenvs.in-project true
   
   # 这个命令会：
   # 1. 修改 Poetry 的配置文件
   #    位置：C:\Users\用户名\AppData\Roaming\pypoetry\config.toml
   # 2. 设置所有新项目的虚拟环境都创建在项目目录的 .venv 文件夹中
   # 3. 这样做的好处是：
   #    - 方便找到和管理每个项目的虚拟环境
   #    - 删除项目时连同虚拟环境一起删除
   #    - 避免多个项目之间的环境冲突
   ```

### 为什么要这样配置？

1. 为什么使用 pip install cookiecutter？
   - pip 是 Python 的包管理器，它会：
     - 自动处理依赖关系
     - 将工具安装到正确的位置
     - 确保工具可以在命令行中使用

2. 为什么要验证版本？
   - 确保工具安装成功
   - 知道当前使用的是什么版本
   - 方便日后排查问题

3. 为什么要配置 Poetry 的虚拟环境位置？
   - 默认情况下，Poetry 会将所有虚拟环境存放在一个统一的位置
   - 这样不方便项目管理和迁移
   - 将虚拟环境放在项目目录中更容易管理

### 如何检查安装位置？

1. 查看 Python 包的安装位置：
   ```bash
   # 显示 Python 的安装路径
   where python
   
   # 显示包的安装路径
   python -c "import site; print(site.getsitepackages())"
   ```

2. 查看 Poetry 的安装位置：
   ```bash
   # 显示 Poetry 可执行文件的位置
   where poetry
   
   # 显示 Poetry 的配置
   poetry config --list
   ```

### 常见问题

1. 如果看到 "不是内部或外部命令"：
   - 检查环境变量 Path 是否包含：
     - Python 的 Scripts 目录
     - Poetry 的安装目录

2. 如果安装失败：
   - 使用管理员权限运行命令
   - 检查网络连接
   - 检查防火墙设置

### 步骤 4：使用项目模板创建新项目

1. 进入工作目录：
   ```powershell
   cd D:\my_projects
   ```

2. 使用模板创建新项目：
   ```powershell
   cookiecutter D:\data\work\cookiecutter-python-template
   ```

3. 按照提示填写项目信息：
   - project_name: 项目名称
   - project_slug: 项目标识符（通常与项目名称相同）
   - package_name: 包名（通常与项目标识符相同）
   - project_description: 项目描述
   - full_name: 你的名字
   - email: 你的邮箱
   - github_username: GitHub用户名
   - version: 版本号（默认0.1.0）
   - 其他选项根据需要选择

4. 等待项目创建完成

#### 常见问题及解决方案

1. Git相关错误：
   - 错误信息：`FatalError: git failed. Is it installed, and are you in a Git repository directory?`
   - 解决方案：
     - 确保已安装Git
     - 确保Git已添加到系统环境变量
     - 运行 `git --version` 验证Git安装

2. pre-commit相关错误：
   - 错误信息：`Failed to set up Poetry environment: Command '['poetry', 'run', 'pre-commit', 'install']' returned non-zero exit status 1`
   - 解决方案：
     - 这个错误通常不会影响项目创建
     - 项目创建完成后可以手动运行 `poetry run pre-commit install`

3. 项目创建失败：
   - 检查磁盘空间是否充足
   - 确保有写入权限
   - 尝试以管理员身份运行PowerShell
   - 检查Python和Poetry是否正确安装

4. 文件权限问题：
   - 确保对目标目录有写入权限
   - 检查防病毒软件是否阻止了文件操作
   - 尝试关闭可能占用文件的程序

5. 网络问题：
   - 确保能够访问GitHub
   - 检查网络代理设置
   - 如果使用VPN，确保VPN正常工作

#### 验证项目创建

1. 检查项目目录：
   ```powershell
   cd <project_name>
   dir
   ```

2. 确认关键文件存在：
   - pyproject.toml
   - README.md
   - src/<package_name>/
   - tests/
   - docs/

3. 初始化项目环境：
   ```powershell
   poetry install
   ```

4. 运行测试：
   ```powershell
   poetry run pytest
   ```

### 步骤 5：编写第一个程序

1. 创建你的第一个 Python 文件：
```bash
# 使用记事本创建文件
notepad my_first_project/hello.py
```

2. 在文件中输入这些内容：
```python
def greet(name):
    """向指定的人说你好。
    
    Args:
        name: 要问候的人的名字
    
    Returns:
        包含问候语的字符串
    """
    return f"你好，{name}！"

# 测试这个函数
if __name__ == "__main__":
    print(greet("小明"))
```

3. 运行这个程序：
```bash
poetry run python my_first_project/hello.py
```

你应该会看到：`你好，小明！`

### 步骤 6：使用项目环境

1. 激活虚拟环境：
```bash
# 在 PowerShell 中运行
poetry shell
```

你会看到命令提示符变成了这样：
```
(.venv) PS D:\my_projects\my-first-project>
```

2. 安装一个新的包：
```bash
poetry add requests
```

你会看到类似这样的输出：
```
Using version ^2.31.0 for requests
Updating dependencies
Resolving dependencies... (0.3s)
Writing lock file

Package operations: 5 installs, 0 updates, 0 removals

  • Installing certifi (2024.2.2)
  • Installing charset-normalizer (3.3.2)
  • Installing idna (3.6)
  • Installing urllib3 (2.2.1)
  • Installing requests (2.31.0)
```

### 常见问题解决

1. 如果看到 "权限不足" 错误：
   - 以管理员身份运行 PowerShell
   - 右键点击 PowerShell 图标
   - 选择"以管理员身份运行"

2. 如果 Poetry 命令不可用：
   - 关闭并重新打开 PowerShell
   - 确保 Python 已正确添加到 PATH

3. 如果虚拟环境激活失败：
```bash
# 删除现有的虚拟环境
rm -r .venv
# 重新创建
poetry install
```

### 下一步

完成这些基础步骤后，你就可以：
1. 创建自己的 Python 项目
2. 管理项目依赖
3. 运行 Python 程序

准备好后，我们可以继续学习：
- 如何编写测试
- 如何使用代码检查工具
- 如何编写项目文档
- 如何使用版本控制

每个步骤都会像这样详细地解释，让你能轻松跟着操作。

需要继续学习下一部分吗？

## 故障排除指南

### 1. 安装 Python 时的常见问题

1. 提示 "无法访问此网站"：
   - ✅ 解决方法：
     - 使用备用下载地址：https://npm.taobao.org/mirrors/python/
     - 或使用国内镜像：https://registry.npmmirror.com/binary.html?path=python/

2. 安装后输入 `python --version` 仍提示 "不是内部或外部命令"：
   - ✅ 解决方法：
     ```bash
     # 1. 检查 Python 是否正确安装在这些位置之一：
     C:\Users\你的用户名\AppData\Local\Programs\Python\Python311
     C:\Program Files\Python311
     
     # 2. 手动添加到环境变量：
     # - 右键"此电脑" -> 属性 -> 高级系统设置 -> 环境变量
     # - 在"系统变量"中找到 Path
     # - 添加 Python 安装目录和 Scripts 目录
     ```

### 2. Poetry 相关问题

1. 安装 Poetry 时出现 "权限不足"：
   ```bash
   # ❌ 错误信息：
   权限不足，请以管理员身份运行
   
   # ✅ 解决方法：
   # 方法1：以管理员身份运行 PowerShell
   # 方法2：使用用户级安装
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python - --user
   ```