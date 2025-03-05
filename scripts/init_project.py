#!/usr/bin/env python
"""项目初始化脚本."""
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

import click
from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()


def validate_project_name(name: str) -> bool:
    """验证项目名称.

    Args:
        name: 项目名称

    Returns:
        是否有效
    """
    return bool(re.match(r'^[a-zA-Z][\w-]*$', name))


def update_file_content(file_path: Path, replacements: Dict[str, str]) -> None:
    """更新文件内容.

    Args:
        file_path: 文件路径
        replacements: 替换映射
    """
    if not file_path.exists():
        return

    content = file_path.read_text(encoding='utf-8')
    for old, new in replacements.items():
        content = content.replace(old, new)
    file_path.write_text(content, encoding='utf-8')


def run_command(command: List[str], cwd: Optional[Path] = None) -> bool:
    """运行命令.

    Args:
        command: 命令列表
        cwd: 工作目录

    Returns:
        是否成功
    """
    try:
        subprocess.run(command, check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError:
        return False


@click.command()
@click.argument('project_name', required=False)
@click.option('--directory', '-d', help='项目目录', type=click.Path())
@click.option('--description', help='项目描述')
@click.option('--author', help='作者名称')
@click.option('--email', help='作者邮箱')
def init_project(
    project_name: Optional[str],
    directory: Optional[str],
    description: Optional[str],
    author: Optional[str],
    email: Optional[str]
) -> None:
    """初始化新项目."""
    console.print("[bold blue]Python项目初始化向导[/bold blue]")

    # 获取项目信息
    if not project_name:
        project_name = Prompt.ask("请输入项目名称")
    while not validate_project_name(project_name):
        console.print("[red]项目名称无效，只能包含字母、数字、下划线和连字符，且必须以字母开头[/red]")
        project_name = Prompt.ask("请重新输入项目名称")

    if not description:
        description = Prompt.ask("请输入项目描述", default="A Python project")

    if not author:
        author = Prompt.ask("请输入作者名称")

    if not email:
        email = Prompt.ask("请输入作者邮箱")

    # 确定项目目录
    if directory:
        project_dir = Path(directory) / project_name
    else:
        project_dir = Path.cwd() / project_name

    if project_dir.exists():
        if not Confirm.ask(f"目录 {project_dir} 已存在，是否继续？"):
            sys.exit(1)
    else:
        project_dir.mkdir(parents=True)

    # 复制模板文件
    template_dir = Path(__file__).parent.parent
    ignore_patterns = shutil.ignore_patterns(
        '.git*', '__pycache__', '*.pyc', '*.pyo', '*.pyd',
        '.Python', 'build', 'dist', '*.egg-info'
    )
    shutil.copytree(template_dir, project_dir, dirs_exist_ok=True, ignore=ignore_patterns)

    # 更新文件内容
    replacements = {
        'python-project-template': project_name,
        'A modern Python project template': description,
        'Your Name': author,
        'your.email@example.com': email
    }

    files_to_update = [
        project_dir / 'pyproject.toml',
        project_dir / 'README.md',
        project_dir / 'docs/conf.py'
    ]

    for file_path in files_to_update:
        update_file_content(file_path, replacements)

    # 初始化Git仓库
    if not (project_dir / '.git').exists():
        if Confirm.ask("是否初始化Git仓库？", default=True):
            if run_command(['git', 'init'], project_dir):
                console.print("[green]Git仓库初始化成功[/green]")
            else:
                console.print("[red]Git仓库初始化失败[/red]")

    # 安装依赖
    if Confirm.ask("是否安装项目依赖？", default=True):
        if run_command(['poetry', 'install'], project_dir):
            console.print("[green]依赖安装成功[/green]")
        else:
            console.print("[red]依赖安装失败，请手动运行 'poetry install'[/red]")

    # 安装pre-commit钩子
    if Confirm.ask("是否安装pre-commit钩子？", default=True):
        if run_command(['poetry', 'run', 'pre-commit', 'install'], project_dir):
            console.print("[green]pre-commit钩子安装成功[/green]")
        else:
            console.print("[red]pre-commit钩子安装失败，请手动运行 'pre-commit install'[/red]")

    console.print("\n[bold green]项目初始化完成！[/bold green]")
    console.print(f"\n开始使用你的新项目：\n")
    console.print(f"    cd {project_name}")
    console.print(f"    poetry shell")
    console.print(f"    pytest")


if __name__ == '__main__':
    init_project()
