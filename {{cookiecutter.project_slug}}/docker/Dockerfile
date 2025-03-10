# 使用多阶段构建以减小最终镜像的大小
FROM python:3.8-slim as builder

# 设置环境变量
# PYTHONUNBUFFERED：禁用输出缓冲
# PYTHONDONTWRITEBYTECODE：禁用编译后的Python文件
# PIP_NO_CACHE_DIR：禁用pip缓存
# PIP_DISABLE_PIP_VERSION_CHECK：禁用pip版本检查
# POETRY_VERSION：设置Poetry版本
# POETRY_HOME：设置Poetry安装目录
# POETRY_VIRTUALENVS_IN_PROJECT：启用项目内虚拟环境
# POETRY_NO_INTERACTION：禁用Poetry交互模式
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.4.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# 将Poetry添加到PATH中
ENV PATH="$POETRY_HOME/bin:$PATH"

# 安装系统依赖
# apt-get update：更新软件包列表
# apt-get install：安装软件包
# rm -rf /var/lib/apt/lists/*：清理apt缓存
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# 设置工作目录
WORKDIR /app

# 仅复制依赖文件以缓存它们在docker层中
COPY poetry.lock pyproject.toml ./

# 安装依赖
# poetry install：安装依赖
# --no-dev：不安装开发依赖
# --no-root：不使用root用户安装
RUN poetry install --no-dev --no-root

# 复制项目文件
COPY . .

# 安装项目
RUN poetry install --no-dev

# 生产阶段
FROM python:3.8-slim

# 设置环境变量
# PYTHONUNBUFFERED：禁用输出缓冲
# PYTHONDONTWRITEBYTECODE：禁用编译后的Python文件
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 设置工作目录
WORKDIR /app

# 从构建器复制虚拟环境
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# 将虚拟环境添加到PATH中
ENV PATH="/app/.venv/bin:$PATH"

# 创建非根用户
# useradd：创建用户
# -m：创建用户主目录
# -s /bin/bash：设置用户shell
# chown：更改文件所有权
RUN useradd -m -s /bin/bash app_user \
    && chown -R app_user:app_user /app

# 切换到非根用户
USER app_user

# 运行应用程序的命令
CMD ["python", "-m", "src"]
