"""项目管理相关的工具函数。"""
import os
import shutil
from pathlib import Path
from typing import Optional

from .command import run_command


def init_git(project_dir: Path) -> bool:
    """
    初始化 Git 仓库。

    Args:
        project_dir: 项目目录

    Returns:
        bool: 是否初始化成功
    """
    try:
        # 删除现有的 .git 目录
        git_dir = project_dir / ".git"
        if git_dir.exists():
            try:
                shutil.rmtree(git_dir)
            except PermissionError:
                # 如果遇到权限错误，尝试修改文件权限
                for root, dirs, files in os.walk(git_dir):
                    for d in dirs:
                        os.chmod(Path(root) / d, 0o777)
                    for f in files:
                        os.chmod(Path(root) / f, 0o777)
                shutil.rmtree(git_dir)

        # 初始化 Git 仓库
        code, _, err = run_command("git init", cwd=project_dir)
        if code != 0:
            print(f"[ERROR] Git 初始化失败: {err}")
            return False

        # 添加文件
        code, _, err = run_command("git add .", cwd=project_dir)
        if code != 0:
            print(f"[ERROR] Git add 失败: {err}")
            return False

        # 提交
        code, _, err = run_command(
            'git commit -m "Initial commit"',
            cwd=project_dir
        )
        if code != 0:
            print(f"[ERROR] Git commit 失败: {err}")
            return False

        return True
    except Exception as e:
        print(f"[ERROR] Git 初始化出错: {e}")
        return False


def setup_pre_commit(project_dir: Path) -> bool:
    """
    配置 pre-commit。

    Args:
        project_dir: 项目目录

    Returns:
        bool: 是否配置成功
    """
    try:
        code, _, err = run_command(
            "poetry run pre-commit install",
            cwd=project_dir
        )
        if code != 0:
            print(f"[ERROR] pre-commit 安装失败: {err}")
            return False

        return True
    except Exception as e:
        print(f"[ERROR] pre-commit 配置出错: {e}")
        return False


def create_venv(project_dir: Path) -> bool:
    """
    创建虚拟环境。

    Args:
        project_dir: 项目目录

    Returns:
        bool: 是否创建成功
    """
    try:
        code, _, err = run_command(
            "poetry env use python",
            cwd=project_dir
        )
        if code != 0:
            print(f"[ERROR] 虚拟环境创建失败: {err}")
            return False

        return True
    except Exception as e:
        print(f"[ERROR] 虚拟环境创建出错: {e}")
        return False 