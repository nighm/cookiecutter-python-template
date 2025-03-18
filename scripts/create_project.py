#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目创建自动化脚本
用于自动化执行项目模板文档中的所有步骤
"""
import argparse
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, Tuple

def run_command(command: str, cwd: Optional[Path] = None, retry: int = 3) -> Tuple[int, str, str]:
    """运行命令并返回结果"""
    print(f"[DEBUG] 执行命令: {command}")
    if cwd:
        print(f"[DEBUG] 工作目录: {cwd}")
    
    for i in range(retry):
        try:
            if i > 0:
                print(f"[DEBUG] 第 {i + 1} 次尝试...")
            
            # 设置环境变量以处理编码问题
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
                env=env,
                encoding='utf-8'
            )
            
            print(f"[DEBUG] 命令返回码: {result.returncode}")
            if result.stdout:
                print(f"[DEBUG] 标准输出:\n{result.stdout.strip()}")
            if result.stderr:
                print(f"[DEBUG] 错误输出:\n{result.stderr.strip()}")
            
            # 如果命令成功或者不是网络错误，直接返回
            if result.returncode == 0 or "connect to pypi.org failed" not in result.stderr:
                return result.returncode, result.stdout, result.stderr
            
            # 如果是网络错误且还有重试次数，等待后重试
            if i < retry - 1:
                print(f"[WARN] 网络错误，{i + 1}/{retry} 次重试...")
                time.sleep(2 ** i)  # 指数退避
                continue
            
            return result.returncode, result.stdout, result.stderr
            
        except Exception as e:
            print(f"[ERROR] 执行出错: {str(e)}")
            if i < retry - 1:
                print(f"[WARN] 执行出错，{i + 1}/{retry} 次重试...")
                time.sleep(2 ** i)
                continue
            return 1, "", str(e)

def print_step(step: str) -> None:
    """打印步骤信息"""
    print(f"\n{'='*20} {step} {'='*20}")

def check_prerequisites() -> bool:
    """检查必要工具是否已安装"""
    tools = {
        "python": "python --version",
        "poetry": "poetry --version",
        "cookiecutter": "cookiecutter --version",
    }
    
    all_installed = True
    print_step("检查必要工具")
    
    for tool, command in tools.items():
        code, out, err = run_command(command)
        if code == 0:
            print(f"[OK] {tool} 已安装: {out.strip()}")
        else:
            print(f"[ERROR] {tool} 未安装或有错误")
            all_installed = False
    
    return all_installed

def setup_poetry_source() -> None:
    """配置 Poetry 镜像源"""
    print_step("配置 Poetry 镜像源")
    
    # 检查当前配置
    print("[DEBUG] 检查当前 Poetry 配置...")
    code, out, err = run_command("poetry config --list", retry=1)
    
    # 移除已有的源配置
    print("[DEBUG] 尝试移除已有的镜像源配置...")
    run_command("poetry source remove tuna", retry=1)
    run_command("poetry source remove aliyun", retry=1)
    
    # 添加清华镜像源
    print("[DEBUG] 尝试添加清华镜像源...")
    code, out, err = run_command("poetry source add tuna https://pypi.tuna.tsinghua.edu.cn/simple/")
    if code != 0:
        print("[WARN] 添加清华镜像源失败，尝试使用阿里云源...")
        code, out, err = run_command("poetry source add aliyun https://mirrors.aliyun.com/pypi/simple/")
        if code != 0:
            print("[WARN] 添加镜像源失败，将使用默认源")
    
    # 限制并发数以避免网络问题
    print("[DEBUG] 配置安装器参数...")
    run_command("poetry config installer.max-workers 1")
    
    # 验证配置
    print("[DEBUG] 验证最终配置...")
    run_command("poetry config --list", retry=1)

def create_project(project_name: str, output_dir: Path) -> Optional[Path]:
    """创建新项目"""
    print_step(f"创建项目: {project_name}")
    
    # 检查目录状态
    print(f"[DEBUG] 检查输出目录: {output_dir}")
    if output_dir.exists():
        print(f"[DEBUG] 目录已存在，包含: {[f.name for f in output_dir.iterdir()]}")
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 检查目标项目目录
    project_slug = project_name.lower().replace(" ", "_")
    target_dir = output_dir / project_slug
    if target_dir.exists():
        print(f"[WARN] 目标项目目录已存在: {target_dir}")
        print(f"[DEBUG] 目录内容: {[f.name for f in target_dir.iterdir()]}")
    
    # 创建项目
    command = (
        f'cookiecutter https://github.com/nighm/cookiecutter-python-template.git '
        f'--no-input '
        f'project_name="{project_name}" '
        f'project_slug="{project_slug}" '
    )
    
    code, out, err = run_command(command, output_dir)
    if code != 0:
        print(f"[ERROR] 创建项目失败，请检查上述详细输出")
        return None
    
    # 验证项目创建
    if not target_dir.exists():
        print(f"[ERROR] 项目目录未创建: {target_dir}")
        return None
    
    print(f"[INFO] 项目目录已创建: {target_dir}")
    print(f"[DEBUG] 项目文件列表:")
    for item in target_dir.rglob("*"):
        if item.is_file():
            print(f"  - {item.relative_to(target_dir)}")
    
    return target_dir

def initialize_project(project_dir: Path) -> bool:
    """初始化项目"""
    print_step("初始化项目")
    
    # 检查项目目录
    print(f"[DEBUG] 检查项目目录: {project_dir}")
    if not project_dir.exists():
        print(f"[ERROR] 项目目录不存在")
        return False
    
    # 检查 pyproject.toml
    pyproject = project_dir / "pyproject.toml"
    if not pyproject.exists():
        print(f"[ERROR] pyproject.toml 不存在")
        return False
    
    print(f"[DEBUG] pyproject.toml 内容:")
    with open(pyproject, 'r', encoding='utf-8') as f:
        print(f.read())
    
    # 安装依赖
    print("[INFO] 安装项目依赖...")
    code, out, err = run_command("poetry install", project_dir)
    if code != 0:
        print(f"[ERROR] 安装依赖失败，请检查上述详细输出")
        return False
    
    # 检查虚拟环境
    print("[DEBUG] 检查虚拟环境...")
    run_command("poetry env info", project_dir)
    
    # 安装 pre-commit 钩子
    print("[INFO] 安装 pre-commit 钩子...")
    code, out, err = run_command("poetry run pre-commit install", project_dir)
    if code != 0:
        print(f"[ERROR] 安装 pre-commit 钩子失败，请检查上述详细输出")
        return False
    
    # 检查 pre-commit 配置
    precommit_config = project_dir / ".pre-commit-config.yaml"
    if precommit_config.exists():
        print(f"[DEBUG] .pre-commit-config.yaml 内容:")
        with open(precommit_config, 'r', encoding='utf-8') as f:
            print(f.read())
    
    # 运行测试
    print("[INFO] 运行测试...")
    code, out, err = run_command("poetry run pytest -v", project_dir)
    if code != 0:
        print(f"[WARN] 部分测试未通过，请检查上述详细输出")
    
    return True

def main() -> int:
    """主函数"""
    start_time = time.time()
    
    # 设置输出编码
    if sys.platform == "win32":
        print("[DEBUG] 配置 Windows 编码...")
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="Python项目创建工具")
    parser.add_argument("project_name", help="项目名称")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.home() / "projects",
        help="项目输出目录 (默认: ~/projects)"
    )
    
    args = parser.parse_args()
    print(f"[DEBUG] 项目名称: {args.project_name}")
    print(f"[DEBUG] 输出目录: {args.output_dir}")
    
    # 检查必要工具
    if not check_prerequisites():
        print("\n[ERROR] 请先安装所需工具后重试")
        return 1
    
    # 配置 Poetry 镜像源
    setup_poetry_source()
    
    # 创建项目
    project_dir = create_project(args.project_name, args.output_dir)
    if not project_dir:
        return 1
    
    # 初始化项目
    if not initialize_project(project_dir):
        return 1
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n[SUCCESS] 项目创建成功！")
    print(f"[INFO] 项目位置: {project_dir}")
    print(f"[INFO] 总耗时: {duration:.1f} 秒")
    print("\n[INFO] 下一步:")
    print(f"  cd {project_dir}")
    print("  poetry shell  # 激活虚拟环境")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 