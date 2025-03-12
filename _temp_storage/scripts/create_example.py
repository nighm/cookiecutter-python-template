#!/usr/bin/env python
"""创建示例代码脚本."""
import os
import shutil
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.prompt import Confirm

console = Console()

EXAMPLE_TYPES = {
    "fastapi": "FastAPI Web应用示例",
    "cli": "CLI工具示例",
    "task": "后台任务示例",
    "orm": "SQLAlchemy ORM示例",
    "cache": "Redis缓存示例",
    "all": "所有示例",
}


def copy_example(src_dir: Path, dst_dir: Path, example_type: str) -> None:
    """复制示例代码.

    Args:
        src_dir: 源目录
        dst_dir: 目标目录
        example_type: 示例类型
    """
    example_dir = src_dir / "examples"
    if not example_dir.exists():
        console.print(f"[red]示例目录 {example_dir} 不存在[/red]")
        return

    if example_type == "all":
        # 复制所有示例
        for item in example_dir.iterdir():
            if item.is_file() and item.suffix == ".py":
                shutil.copy2(item, dst_dir)
        console.print("[green]已复制所有示例代码[/green]")
    else:
        # 复制特定示例
        example_file = example_dir / f"{example_type}_demo.py"
        if example_file.exists():
            shutil.copy2(example_file, dst_dir)
            console.print(f"[green]已复制 {example_type} 示例代码[/green]")
        else:
            console.print(f"[red]示例文件 {example_file} 不存在[/red]")


@click.command()
@click.argument("example_type", type=click.Choice(list(EXAMPLE_TYPES.keys())))
@click.option("--directory", "-d", help="目标目录", type=click.Path())
def create_example(example_type: str, directory: Optional[str]) -> None:
    """创建示例代码.

    Args:
        example_type: 示例类型
        directory: 目标目录
    """
    console.print(f"[bold blue]创建{EXAMPLE_TYPES[example_type]}[/bold blue]")

    # 确定目标目录
    if directory:
        dst_dir = Path(directory)
    else:
        dst_dir = Path.cwd()

    if not dst_dir.exists():
        if Confirm.ask(f"目录 {dst_dir} 不存在，是否创建？"):
            dst_dir.mkdir(parents=True)
        else:
            return

    # 获取模板目录
    template_dir = Path(__file__).parent.parent

    # 复制示例代码
    copy_example(template_dir, dst_dir, example_type)

    # 创建依赖文件
    if example_type in ["fastapi", "all"]:
        requirements = [
            "fastapi",
            "uvicorn",
            "python-multipart",
            "python-jose[cryptography]",
            "passlib[bcrypt]",
        ]
        with open(dst_dir / "requirements.txt", "a") as f:
            f.write("\n".join(requirements))
        console.print("[green]已添加FastAPI相关依赖[/green]")

    # 添加说明文件
    readme = dst_dir / "README.md"
    if not readme.exists():
        with open(readme, "w", encoding="utf-8") as f:
            f.write(f"# {EXAMPLE_TYPES[example_type]}\n\n")
            f.write("## 使用方法\n\n")
            if example_type == "fastapi":
                f.write("1. 安装依赖\n")
                f.write("```bash\n")
                f.write("pip install -r requirements.txt\n")
                f.write("```\n\n")
                f.write("2. 运行应用\n")
                f.write("```bash\n")
                f.write("uvicorn app:app --reload\n")
                f.write("```\n")
            elif example_type == "cli":
                f.write("运行CLI工具：\n")
                f.write("```bash\n")
                f.write("python cli_demo.py --help\n")
                f.write("```\n")
        console.print("[green]已创建README.md[/green]")

    console.print("\n[bold green]示例代码创建完成！[/bold green]")


if __name__ == "__main__":
    create_example()
