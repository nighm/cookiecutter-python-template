使用指南
========

环境设置
-------

开发环境要求
^^^^^^^^^^

* Python 3.8+
* Poetry
* Git
* Make（可选）
* Docker（可选）

安装步骤
^^^^^^^

1. 克隆项目::

    git clone <repository-url>

2. 安装Poetry::

    curl -sSL https://install.python-poetry.org | python3 -

3. 初始化环境::

    poetry install

4. 安装pre-commit hooks::

    poetry run pre-commit install

项目配置
-------

环境变量
^^^^^^^

项目使用 `python-dotenv` 管理环境变量。创建 `.env` 文件：

.. code-block:: ini

    APP_ENV=development
    APP_DEBUG=true
    LOG_LEVEL=INFO
    LOG_FORMAT=console
    DEFAULT_LANGUAGE=zh

配置文件
^^^^^^^

主要配置文件位于 `src/config` 目录：

* `settings.py`: 全局设置
* `logging.py`: 日志配置
* `i18n.py`: 国际化配置

开发工具
-------

代码格式化
^^^^^^^^

使用black格式化代码::

    make format

代码检查
^^^^^^^

运行代码质量检查::

    make lint

运行测试
^^^^^^^

执行单元测试::

    make test

构建文档
^^^^^^^

生成项目文档::

    make docs

常见问题
-------

1. 环境问题
^^^^^^^^^

Q: Poetry安装失败？
A: 检查Python版本是否满足要求，尝试使用pip安装：`pip install poetry`

2. 依赖问题
^^^^^^^^^

Q: 依赖安装失败？
A: 尝试清除缓存后重新安装：`poetry cache clear . --all`

3. 编码问题
^^^^^^^^^

Q: 出现编码错误？
A: 确保所有Python文件使用UTF-8编码，检查环境变量 `PYTHONIOENCODING=utf-8`
