#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目创建自动化脚本
用于自动化执行项目模板文档中的所有步骤
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

# 缓存配置
CACHE_DIR = Path.home() / ".python_project_cache"
TEMPLATE_CACHE_DIR = CACHE_DIR / "templates"
TOOLS_CACHE_DIR = CACHE_DIR / "tools"
CACHE_CONFIG_FILE = CACHE_DIR / "cache_config.json"
CACHE_VALIDITY_DAYS = 7  # 缓存有效期（天）

def setup_cache_dirs() -> None:
    """初始化缓存目录"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TOOLS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    if not CACHE_CONFIG_FILE.exists():
        cache_config = {
            "last_update": "",
            "template_version": "",
            "tools_versions": {},
            "dependencies_hash": ""
        }
        save_cache_config(cache_config)

def save_cache_config(config: Dict) -> None:
    """保存缓存配置"""
    with open(CACHE_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def load_cache_config() -> Dict:
    """加载缓存配置"""
    if CACHE_CONFIG_FILE.exists():
        with open(CACHE_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def is_cache_valid() -> bool:
    """检查缓存是否有效"""
    config = load_cache_config()
    if not config.get("last_update"):
        return False
    
    last_update = datetime.fromisoformat(config["last_update"])
    return datetime.now() - last_update < timedelta(days=CACHE_VALIDITY_DAYS)

def get_template_version(template_dir: Optional[Path] = None) -> str:
    """获取模板版本"""
    if template_dir and template_dir.exists():
        code, out, _ = run_command("git rev-parse HEAD", template_dir)
        if code == 0:
            return out.strip()
    return ""

def check_template_updates() -> bool:
    """检查模板是否有更新"""
    print("[DEBUG] 检查模板更新...")
    
    # 获取本地版本
    local_version = get_template_version(TEMPLATE_CACHE_DIR)
    if not local_version:
        print("[DEBUG] 本地模板不存在或无法获取版本")
        return True
    
    # 获取远程版本
    template_url = "https://github.com/nighm/cookiecutter-python-template.git"
    code, out, _ = run_command(f"git ls-remote {template_url} HEAD")
    if code != 0:
        print("[WARN] 无法获取远程版本，将使用本地缓存")
        return False
    
    remote_version = out.split()[0] if out else ""
    if not remote_version:
        print("[WARN] 无法解析远程版本，将使用本地缓存")
        return False
    
    # 比较版本
    if local_version != remote_version:
        print(f"[INFO] 发现模板更新: {local_version[:8]} -> {remote_version[:8]}")
        return True
    
    print("[INFO] 模板已是最新版本")
    return False

def update_template_cache() -> None:
    """更新模板缓存"""
    print("[INFO] 更新模板缓存...")
    template_url = "https://github.com/nighm/cookiecutter-python-template.git"
    
    if TEMPLATE_CACHE_DIR.exists():
        # 检查是否需要更新
        if not check_template_updates():
            return
        
        # 更新已存在的模板
        code, _, _ = run_command("git pull", TEMPLATE_CACHE_DIR)
        if code == 0:
            print("[INFO] 模板缓存更新成功")
            
            # 更新缓存配置
            config = load_cache_config()
            config["template_version"] = get_template_version(TEMPLATE_CACHE_DIR)
            save_cache_config(config)
            return
        
        # 如果更新失败，删除后重新克隆
        shutil.rmtree(TEMPLATE_CACHE_DIR)
    
    # 克隆模板
    code, _, _ = run_command(f"git clone {template_url} {TEMPLATE_CACHE_DIR}")
    if code == 0:
        print("[INFO] 模板缓存克隆成功")
        
        # 保存版本信息
        config = load_cache_config()
        config["template_version"] = get_template_version(TEMPLATE_CACHE_DIR)
        save_cache_config(config)
    else:
        print("[WARN] 模板缓存更新失败，将使用在线模板")

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
    
    # 添加镜像源（按优先级尝试）
    sources = [
        ("tuna", "https://pypi.tuna.tsinghua.edu.cn/simple/"),
        ("aliyun", "https://mirrors.aliyun.com/pypi/simple/"),
        ("douban", "https://pypi.doubanio.com/simple/")
    ]
    
    success = False
    for name, url in sources:
        print(f"[DEBUG] 尝试添加{name}镜像源...")
        code, out, err = run_command(f"poetry source add {name} {url}")
        if code == 0:
            print(f"[INFO] 成功添加{name}镜像源")
            success = True
            break
        else:
            print(f"[WARN] 添加{name}镜像源失败，尝试下一个...")
    
    if not success:
        print("[WARN] 所有镜像源添加失败，将使用默认源")
    
    # 配置安装器参数
    print("[DEBUG] 配置安装器参数...")
    run_command("poetry config installer.max-workers 1")  # 限制并发数
    run_command("poetry config installer.timeout 300")    # 增加超时时间
    
    # 验证配置
    print("[DEBUG] 验证最终配置...")
    run_command("poetry config --list", retry=1)

def remove_readonly(func, path, _):
    """处理只读文件的删除"""
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)

def create_project(project_name: str, output_dir: Path, use_cache: bool = True) -> Optional[Path]:
    """创建新项目"""
    print_step(f"创建项目: {project_name}")
    
    # 检查并更新缓存
    if use_cache and not is_cache_valid():
        print("[INFO] 缓存已过期，正在更新...")
        setup_cache_dirs()
        update_template_cache()
        
        # 更新缓存配置
        config = load_cache_config()
        config["last_update"] = datetime.now().isoformat()
        save_cache_config(config)
    
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
        
        # 询问用户是否删除
        while True:
            response = input("\n是否删除已存在的项目目录？[y/N] ").lower().strip()
            if response in ['y', 'yes']:
                print("[INFO] 删除已存在的项目目录...")
                try:
                    import shutil
                    # 先尝试删除 .git 目录
                    git_dir = target_dir / '.git'
                    if git_dir.exists():
                        print("[DEBUG] 删除 .git 目录...")
                        shutil.rmtree(git_dir, onerror=remove_readonly)
                    
                    # 删除整个项目目录
                    print("[DEBUG] 删除项目目录...")
                    shutil.rmtree(target_dir, onerror=remove_readonly)
                    print("[INFO] 目录删除成功")
                    break
                except Exception as e:
                    print(f"[ERROR] 删除目录失败: {e}")
                    return None
            elif response in ['', 'n', 'no']:
                print("[INFO] 取消操作")
                return None
            else:
                print("[ERROR] 无效的输入，请输入 y 或 n")
    
    # 创建项目
    if use_cache and TEMPLATE_CACHE_DIR.exists():
        print("[INFO] 使用缓存的模板创建项目...")
        command = (
            f'cookiecutter {TEMPLATE_CACHE_DIR} '
            f'--no-input '
            f'project_name="{project_name}" '
            f'project_slug="{project_slug}" '
        )
    else:
        print("[INFO] 使用在线模板创建项目...")
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

def check_poetry_cache(project_dir: Path) -> bool:
    """检查 Poetry 依赖缓存状态"""
    print("[DEBUG] 检查 Poetry 依赖缓存...")
    
    # 检查 poetry.lock 文件
    lock_file = project_dir / "poetry.lock"
    if not lock_file.exists():
        print("[DEBUG] 未找到 poetry.lock 文件，需要重新安装依赖")
        return False
    
    # 获取缓存目录
    cache_dir = Path.home() / ".cache" / "pypoetry" / "cache"
    if not cache_dir.exists():
        print("[DEBUG] Poetry 缓存目录不存在，需要重新安装依赖")
        return False
    
    print(f"[INFO] Poetry 缓存目录: {cache_dir}")
    print("[DEBUG] 缓存中的包:")
    for pkg in cache_dir.glob("*/*.whl"):
        print(f"  - {pkg.name}")
    
    return True

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
    
    # 检查依赖缓存
    has_cache = check_poetry_cache(project_dir)
    print(f"[INFO] Poetry 依赖缓存状态: {'已存在' if has_cache else '需要更新'}")
    
    # 安装依赖
    print("[INFO] 安装项目依赖...")
    for i in range(3):  # 最多尝试3次
        if i > 0:
            print(f"[INFO] 第 {i + 1} 次尝试安装依赖...")
        
        if i > 0 or not has_cache:
            # 清理缓存
            print("[DEBUG] 清理 Poetry 缓存...")
            run_command("poetry cache clear . --all", project_dir)
            
            # 更新锁文件
            print("[DEBUG] 更新 Poetry 锁文件...")
            run_command("poetry lock --no-update", project_dir)
        
        # 安装依赖
        code, out, err = run_command("poetry install", project_dir)
        if code == 0:
            print("[INFO] 依赖安装成功")
            break
        elif "connect to pypi.org failed" in err:
            print("[WARN] 网络错误，将重试...")
            time.sleep(2 ** i)  # 指数退避
            continue
        else:
            print(f"[ERROR] 安装依赖失败，请检查上述详细输出")
            return False
    
    # 检查虚拟环境
    print("[DEBUG] 检查虚拟环境...")
    run_command("poetry env info", project_dir)
    
    # 安装 pre-commit 钩子
    print("[INFO] 安装 pre-commit 钩子...")
    code, out, err = run_command("poetry run pre-commit install", project_dir)
    if code != 0:
        print(f"[WARN] 安装 pre-commit 钩子失败，但这不是致命错误")
    
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
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="不使用缓存，始终从网络获取最新内容"
    )
    
    args = parser.parse_args()
    print(f"[DEBUG] 项目名称: {args.project_name}")
    print(f"[DEBUG] 输出目录: {args.output_dir}")
    print(f"[DEBUG] 使用缓存: {not args.no_cache}")
    
    # 检查必要工具
    if not check_prerequisites():
        print("\n[ERROR] 请先安装所需工具后重试")
        return 1
    
    # 配置 Poetry 镜像源
    setup_poetry_source()
    
    # 创建项目
    project_dir = create_project(args.project_name, args.output_dir, use_cache=not args.no_cache)
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