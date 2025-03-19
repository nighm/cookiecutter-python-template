"""包管理相关的工具函数。"""
from pathlib import Path
from typing import Optional

from .command import run_command


def setup_poetry_source(cwd: Optional[Path] = None) -> bool:
    """
    配置 Poetry 包管理器的源。

    Args:
        cwd: 工作目录

    Returns:
        bool: 是否配置成功
    """
    try:
        # 移除已有的源配置
        code, _, _ = run_command(
            "poetry source remove tuna",
            cwd=cwd,
            retry=1
        )

        # 添加清华源
        code, _, _ = run_command(
            "poetry source add tuna https://pypi.tuna.tsinghua.edu.cn/simple --priority primary",
            cwd=cwd,
            retry=1
        )

        return True
    except Exception as e:
        print(f"[ERROR] 配置 Poetry 源失败: {e}")
        return False


def install_dependencies(cwd: Optional[Path] = None, dev: bool = True) -> bool:
    """
    安装项目依赖。

    Args:
        cwd: 工作目录
        dev: 是否安装开发依赖

    Returns:
        bool: 是否安装成功
    """
    try:
        cmd = "poetry install --no-root"
        if not dev:
            cmd += " --no-dev"

        code, _, err = run_command(cmd, cwd=cwd, retry=3, timeout=600)
        if code != 0:
            print(f"[ERROR] 安装依赖失败: {err}")
            return False

        return True
    except Exception as e:
        print(f"[ERROR] 安装依赖出错: {e}")
        return False 