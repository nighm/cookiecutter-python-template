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
from typing import Any, Dict, Optional, Tuple

from tqdm import tqdm

# 缓存配置
CACHE_DIR = Path.home() / ".python_project_cache"
TEMPLATE_CACHE_DIR = CACHE_DIR / "templates"
TOOLS_CACHE_DIR = CACHE_DIR / "tools"
CACHE_CONFIG_FILE = CACHE_DIR / "cache_config.json"
CACHE_VALIDITY_DAYS = 7  # 缓存有效期（天）


class ProgressSpinner:
    """进度旋转器，用于显示长时间运行任务的进度"""

    def __init__(self, desc: str = "", total: int = 100):
        self.desc = desc
        self.total = total
        self.current = 0
        self.start_time = time.time()
        self.spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.spinner_idx = 0
        self.is_running = False

    def start(self) -> None:
        """开始显示进度"""
        self.is_running = True
        self.start_time = time.time()
        self._update()

    def update(self, n: int = 1) -> None:
        """更新进度"""
        self.current += n
        if self.current > self.total:
            self.current = self.total
        self._update()

    def _update(self) -> None:
        """更新显示"""
        if not self.is_running:
            return

        elapsed = time.time() - self.start_time
        percent = (self.current / self.total) * 100
        spinner = self.spinner_chars[self.spinner_idx]
        self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_chars)

        sys.stdout.write(f"\r{spinner} {self.desc}: {percent:.1f}% [{elapsed:.1f}s]")
        sys.stdout.flush()

    def finish(self) -> None:
        """完成进度显示"""
        self.is_running = False
        sys.stdout.write("\n")
        sys.stdout.flush()


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
            "dependencies_hash": "",
        }
        save_cache_config(cache_config)


def save_cache_config(config: Dict) -> None:
    """保存缓存配置"""
    with open(CACHE_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def load_cache_config() -> Dict:
    """加载缓存配置"""
    if CACHE_CONFIG_FILE.exists():
        with open(CACHE_CONFIG_FILE, "r", encoding="utf-8") as f:
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
    template_url = "git@github.com:nighm/cookiecutter-python-template.git"
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
    code, out, _ = run_command(f"git clone {template_url} {TEMPLATE_CACHE_DIR}", cwd=str(CACHE_DIR))

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


def handle_git_error(error_msg: str) -> Optional[str]:
    """处理Git错误并返回建议的解决方案"""
    error_msg = error_msg.lower()

    error_patterns = {
        "authentication failed": "Git认证失败，请检查凭证设置",
        "could not resolve host": "DNS解析失败，请检查网络连接和代理设置",
        "ssl connect error": "SSL连接错误，请检查网络设置或证书配置",
        "timeout": "连接超时，请检查网络状态",
        "repository not found": "仓库未找到，请检查URL是否正确",
        "permission denied": "权限被拒绝，请检查访问权限",
        "filename too long": "文件路径过长，请尝试使用更短的项目名称",
    }

    for pattern, solution in error_patterns.items():
        if pattern in error_msg:
            return solution

    return None


def run_command_with_progress(
    command: str, desc: str, timeout: int = 300
) -> Tuple[int, str, str]:
    """运行命令并显示进度"""
    print(f"[DEBUG] 开始执行: {desc}")
    print(f"[DEBUG] 命令: {command}")
    print(f"[DEBUG] 超时时间: {timeout}秒")

    start_time = time.time()
    process = None
    output = []
    errors = []
    spinner = None

    try:
        # 创建进度显示
        spinner = ProgressSpinner(desc=desc)
        spinner.start()

        # 启动进程
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
            universal_newlines=True,
        )

        # 非阻塞读取输出
        while True:
            # 检查超时
            if time.time() - start_time > timeout:
                process.kill()
                spinner.finish()
                return 1, "", f"命令执行超时（{timeout}秒）"

            # 读取输出
            stdout_line = process.stdout.readline() if process.stdout else ""
            stderr_line = process.stderr.readline() if process.stderr else ""

            if stdout_line:
                output.append(stdout_line)
                print(f"[OUTPUT] {stdout_line.strip()}")
            if stderr_line:
                errors.append(stderr_line)
                print(f"[ERROR] {stderr_line.strip()}")

                # 检查是否有Git错误
                if command.startswith("git "):
                    solution = handle_git_error(stderr_line)
                    if solution:
                        print(f"[HINT] {solution}")

            # 检查进程是否结束
            if process.poll() is not None:
                break

            # 更新进度显示
            spinner.update()
            time.sleep(0.1)

        # 获取剩余输出
        remaining_stdout, remaining_stderr = process.communicate()
        if remaining_stdout:
            output.append(remaining_stdout)
            print(f"[OUTPUT] {remaining_stdout.strip()}")
        if remaining_stderr:
            errors.append(remaining_stderr)
            print(f"[ERROR] {remaining_stderr.strip()}")

        spinner.finish()
        elapsed = time.time() - start_time

        # 打印执行结果
        returncode = process.returncode
        status = "成功" if returncode == 0 else "失败"
        print(f"[INFO] 命令执行{status} (耗时: {elapsed:.1f}秒, 返回码: {returncode})")

        return returncode, "".join(output), "".join(errors)

    except Exception as e:
        if process:
            try:
                process.kill()
            except Exception:
                pass
        if spinner:
            spinner.finish()
        error_msg = str(e)
        print(f"[ERROR] 执行出错: {error_msg}")
        return 1, "", error_msg


def run_command(
    command: str, cwd: Optional[Path] = None, retry: int = 3, timeout: int = 300
) -> Tuple[int, str, str]:
    """运行命令并返回结果"""
    print(f"[DEBUG] 执行命令: {command}")
    if cwd:
        print(f"[DEBUG] 工作目录: {cwd}")
    print(f"[DEBUG] 超时设置: {timeout}秒")

    # Windows系统特殊处理
    is_windows = platform.system().lower() == "windows"
    if is_windows:
        # 处理路径分隔符
        command = command.replace("/", "\\")
        # Git命令特殊处理
        if command.startswith("git "):
            command = f"git -c core.autocrlf=true -c core.longpaths=true {command[4:]}"
            # 添加SSL验证选项
            if "clone" in command or "pull" in command:
                command = command.replace("git ", "git -c http.sslVerify=true ")

    # 设置网络重试参数
    max_retries = retry
    retry_delay = 2
    spinner = None

    try:
        spinner = ProgressSpinner(desc=f"执行命令")
        spinner.start()

        for i in range(max_retries):
            try:
                if i > 0:
                    print(f"[DEBUG] 第 {i + 1} 次尝试...")
                    time.sleep(retry_delay * i)  # 指数退避

                # 设置环境变量以处理编码问题
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8"
                env["PYTHONUTF8"] = "1"
                if is_windows:
                    env["PYTHONLEGACYWINDOWSFSENCODING"] = "0"
                    env["GIT_TERMINAL_PROMPT"] = "0"  # 禁用Git凭证弹窗

                # Windows下处理Poetry命令
                if is_windows and command.startswith("poetry "):
                    command = f"poetry --no-ansi {command[7:]}"

                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    check=False,
                    env=env,
                    encoding="utf-8",
                    timeout=timeout,
                )

                print(f"[DEBUG] 命令返回码: {result.returncode}")
                if result.stdout:
                    print(f"[DEBUG] 标准输出:\n{result.stdout.strip()}")
                if result.stderr:
                    print(f"[DEBUG] 错误输出:\n{result.stderr.strip()}")

                # 处理Windows特定错误
                if is_windows and result.returncode != 0:
                    if any(
                        err in result.stderr.lower()
                        for err in ["拒绝访问", "access is denied", "权限不够"]
                    ):
                        print("[WARN] Windows权限错误，尝试提升权限重试...")
                        continue
                    if (
                        "ssl connect error" in result.stderr.lower()
                        or "could not resolve host" in result.stderr.lower()
                    ):
                        print("[WARN] 网络连接错误，正在重试...")
                        continue
                    if "filename too long" in result.stderr.lower():
                        print("[WARN] 文件路径过长，尝试使用长路径支持...")
                        continue

                # 如果命令成功或者不是网络错误，直接返回
                if (
                    result.returncode == 0
                    or "connect to pypi.org failed" not in result.stderr
                ):
                    return result.returncode, result.stdout, result.stderr

                # 如果是网络错误且还有重试次数，等待后重试
                if i < retry - 1:
                    print(f"[WARN] 网络错误，{i + 1}/{retry} 次重试...")
                    time.sleep(2**i)  # 指数退避
                    continue

                return result.returncode, result.stdout, result.stderr

            except subprocess.TimeoutExpired:
                print(f"[ERROR] 命令执行超时（{timeout}秒）")
                if i < retry - 1:
                    print(f"[WARN] 超时重试，{i + 1}/{retry} 次...")
                    time.sleep(2**i)
                    continue
                return 1, "", f"命令执行超时（{timeout}秒）"
            except KeyboardInterrupt:
                print("\n[INFO] 用户中断执行")
                return 130, "", "User interrupted"
            except Exception as e:
                print(f"[ERROR] 执行出错: {str(e)}")
                if i < retry - 1:
                    print(f"[WARN] 执行出错，{i + 1}/{retry} 次重试...")
                    time.sleep(2**i)
                    continue
                return 1, "", str(e)
    finally:
        if spinner:
            spinner.finish()


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


def clear_poetry_cache():
    """清理 Poetry 缓存，处理权限错误"""
    try:
        run_command("poetry cache clear . --all --no-interaction", retry=1)
    except Exception as e:
        print(f"[WARN] 清理缓存失败: {e}")
        print("[INFO] 继续执行，这不会影响项目创建")


def setup_poetry_source():
    """配置 Poetry 源"""
    print("[INFO] 配置 Poetry 源...")

    # 移除现有源
    try:
        run_command("poetry source remove tuna", retry=1)
    except Exception:
        print("[DEBUG] 移除源失败，可能是源不存在")

    # 添加清华源
    try:
        run_command(
            "poetry source add tuna https://pypi.tuna.tsinghua.edu.cn/simple/ --priority primary",
            retry=1,
        )
        print("[SUCCESS] Poetry 源配置成功")
    except Exception as e:
        print(f"[ERROR] Poetry 源配置失败: {e}")
        print("[WARN] 将使用默认源继续")


def install_dependencies(project_dir: Path):
    """安装项目依赖"""
    print("[INFO] 安装项目依赖...")

    # 清理缓存
    clear_poetry_cache()

    # 确保Poetry配置正确
    print("[DEBUG] 检查Poetry配置...")
    try:
        run_command("poetry config virtualenvs.in-project true", cwd=project_dir, retry=1)
    except Exception as e:
        print(f"[WARN] 设置Poetry配置失败: {e}")

    # 更新锁文件
    print("[DEBUG] 更新 Poetry 锁文件...")
    try:
        run_command("poetry lock", cwd=project_dir, retry=1)
    except Exception as e:
        print(f"[WARN] 更新锁文件失败: {e}")

    # 安装依赖
    max_retries = 3
    for i in range(max_retries):
        try:
            if i > 0:
                print(f"[INFO] 第 {i + 1} 次尝试安装依赖...")
                # 在重试前检查并清理可能存在的问题
                venv_path = project_dir / ".venv"
                if venv_path.exists():
                    print("[DEBUG] 清理已存在的虚拟环境...")
                    try:
                        shutil.rmtree(venv_path)
                    except Exception as e:
                        print(f"[WARN] 清理虚拟环境失败: {e}")

            print("[DEBUG] 开始安装依赖...")
            run_command("poetry install", cwd=project_dir, retry=3)
            print("[SUCCESS] 依赖安装成功")
            return True
        except Exception as e:
            if i < max_retries - 1:
                print(f"[WARN] 安装失败: {e}")
                print("[WARN] 将重试...")
                clear_poetry_cache()
            else:
                print(f"[ERROR] 依赖安装失败: {e}")
                print("[WARN] 继续执行，但部分功能可能无法使用")
                return False


def remove_readonly(func, path, _):
    """处理只读文件的删除"""
    import stat

    os.chmod(path, stat.S_IWRITE)
    func(path)


def check_network_connection() -> bool:
    """检查网络连接状态"""
    print("[DEBUG] 检查网络连接...")

    # 尝试连接GitHub
    test_urls = [
        "https://github.com",
        "https://api.github.com",
        "https://raw.githubusercontent.com",
    ]

    for url in test_urls:
        try:
            import socket
            import urllib.error
            import urllib.request

            # 设置超时
            socket.setdefaulttimeout(10)

            # 创建请求
            req = urllib.request.Request(url, headers={"User-Agent": "Python/3.x"})

            # 尝试连接
            urllib.request.urlopen(req)
            print(f"[DEBUG] 成功连接到 {url}")
            return True

        except urllib.error.URLError as e:
            print(f"[WARN] 连接 {url} 失败: {e.reason}")
        except Exception as e:
            print(f"[WARN] 检查网络时出错: {e}")

    print("[ERROR] 网络连接检查失败")
    return False


def create_project(
    project_name: str, output_dir: Path, use_cache: bool = True
) -> Optional[Path]:
    """创建新项目"""
    print_step(f"创建项目: {project_name}")

    try:
        # 检查网络连接
        if not check_network_connection():
            print("[ERROR] 网络连接异常，请检查网络设置")
            return None

        # 检查输出目录
        print(f"[DEBUG] 检查输出目录: {output_dir}")
        output_dir = output_dir.resolve()  # 转换为绝对路径
        output_dir.mkdir(parents=True, exist_ok=True)

        # 检查最终项目目录
        project_slug = project_name.lower().replace(" ", "_")
        project_dir = output_dir / project_slug

        if project_dir.exists():
            print(f"[WARN] 目标项目目录已存在: {project_dir}")
            try:
                # 列出目录内容
                contents = list(project_dir.iterdir())
                if contents:
                    print(f"[DEBUG] 目录内容: {[p.name for p in contents]}")
                    response = input("是否删除已存在的项目目录？[y/N] ")
                    if response.lower() == "y":
                        print("[INFO] 删除已存在的项目目录...")
                        try:
                            print("[DEBUG] 删除项目目录...")
                            shutil.rmtree(project_dir, onerror=remove_readonly)
                            print("[INFO] 目录删除成功")
                        except Exception as e:
                            print(f"[ERROR] 删除目录失败: {e}")
                            return None
                    else:
                        print("[INFO] 取消操作")
                        return None
                else:
                    print("[DEBUG] 目录为空，将直接使用")
            except Exception as e:
                print(f"[ERROR] 检查目录内容失败: {e}")
                return None

        # 定义创建步骤和预计时间
        steps = [
            ("准备环境", 5, "配置工作目录和环境变量"),
            ("检查模板更新", 10, "检查远程仓库是否有更新"),
            ("克隆模板", 30, "从GitHub克隆项目模板"),
            ("生成项目文件", 15, "基于模板生成项目文件"),
            ("配置依赖", 20, "设置Poetry和项目依赖"),
            ("安装依赖", 40, "安装项目所需的依赖包"),
            ("初始化Git", 5, "初始化Git仓库"),
            ("配置开发工具", 10, "设置pre-commit等开发工具"),
            ("运行测试", 15, "执行初始化测试"),
        ]

        total_time = sum(step[1] for step in steps)

        with tqdm(total=100, desc="总体进度", position=0) as pbar:
            current_progress = 0

            for step_name, step_time, step_desc in steps:
                try:
                    # 创建子进度条
                    print(f"\n[INFO] {step_name}: {step_desc}")

                    with tqdm(
                        total=step_time, desc=f"  {step_name}", position=1, leave=False
                    ) as step_bar:
                        if step_name == "准备环境":
                            # 环境准备
                            for i in range(step_time):
                                time.sleep(0.1)
                                step_bar.update(1)
                                current_progress += 100 / total_time
                                pbar.update(100 / total_time)

                        elif step_name == "检查模板更新":
                            if use_cache:
                                start = time.time()
                                update_template_cache()
                                elapsed = time.time() - start
                                step_bar.update(step_time)
                                current_progress += step_time * 100 / total_time
                                pbar.update(step_time * 100 / total_time)
                                print(f"[DEBUG] 模板更新耗时: {elapsed:.1f}秒")

                        elif step_name == "克隆模板":
                            print("[INFO] 使用在线模板创建项目...")
                            template_url = "https://github.com/nighm/cookiecutter-python-template.git"

                            # 切换到输出目录
                            os.chdir(output_dir)
                            print(f"[DEBUG] 切换到目录: {output_dir}")

                            cookiecutter_cmd = (
                                f"cookiecutter {template_url} --no-input "
                                f'project_name="{project_name}" '
                                f'project_slug="{project_slug}"'
                            )

                            start = time.time()
                            code, out, err = run_command_with_progress(
                                cookiecutter_cmd, desc="克隆模板", timeout=300
                            )
                            elapsed = time.time() - start

                            if code != 0:
                                print(f"[ERROR] 创建项目失败 (耗时: {elapsed:.1f}秒)")
                                print("[ERROR] 详细错误信息:")
                                if out:
                                    print(out)
                                if err:
                                    print(err)
                                return None

                            print(f"[DEBUG] 模板克隆耗时: {elapsed:.1f}秒")
                            step_bar.update(step_time)
                            current_progress += step_time * 100 / total_time
                            pbar.update(step_time * 100 / total_time)

                        elif step_name == "安装依赖":
                            start = time.time()
                            if not install_dependencies(project_dir):
                                print(
                                    f"[ERROR] 依赖安装失败 (耗时: {time.time() - start:.1f}秒)"
                                )
                                return None
                            print(f"[DEBUG] 依赖安装耗时: {time.time() - start:.1f}秒")
                            step_bar.update(step_time)
                            current_progress += step_time * 100 / total_time
                            pbar.update(step_time * 100 / total_time)

                        else:
                            # 其他步骤的进度显示
                            for i in range(step_time):
                                time.sleep(0.1)
                                step_bar.update(1)
                                current_progress += 100 / total_time
                                pbar.update(100 / total_time)
                except Exception as e:
                    print(f"[ERROR] 执行步骤 {step_name} 时出错: {e}")
                    return None

        print(f"\n[SUCCESS] 项目创建成功！")
        print(f"[INFO] 项目位置: {project_dir}")

        return project_dir
    except Exception as e:
        print(f"[ERROR] 项目创建过程中出错: {e}")
        return None


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
    with open(pyproject, "r", encoding="utf-8") as f:
        print(f.read())

    # 检查依赖缓存
    has_cache = check_poetry_cache(project_dir)
    print(f"[INFO] Poetry 依赖缓存状态: {'已存在' if has_cache else '需要更新'}")

    # 安装依赖
    if not install_dependencies(project_dir):
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
        with open(precommit_config, "r", encoding="utf-8") as f:
            print(f.read())

    # 运行测试
    print("[INFO] 运行测试...")
    code, out, err = run_command("poetry run pytest -v", project_dir)
    if code != 0:
        print(f"[WARN] 部分测试未通过，请检查上述详细输出")

    return True


def cache_dependencies() -> bool:
    """预缓存项目依赖"""
    print_step("预缓存项目依赖")
    cache_dir = Path.home() / ".cache" / "pypoetry" / "cache"

    try:
        # 创建临时目录
        temp_dir = Path("temp_cache_project")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()

        print("[INFO] 创建临时项目...")
        # 创建临时 pyproject.toml
        pyproject_content = """
[tool.poetry]
name = "cache-project"
version = "0.1.0"
description = "Temporary project for caching dependencies"
authors = ["cache <cache@example.com>"]

[tool.poetry.dependencies]
python = ">=3.11.0,<3.12.0"
mkdocs = "^1.5.0"
mkdocs-material = "^9.0.0"
mkdocstrings = {extras = ["python"], version = "^0.24.0"}

[tool.poetry.group.dev.dependencies]
black = "^24.2.0"
isort = "^5.13.2"
ruff = "^0.3.0"
mypy = "^1.8.0"
pydocstyle = "^6.3.0"
pytest = "^8.0.0"
pytest-cov = "^4.1.0"
pylint = "^3.0.3"
bandit = "^1.7.7"
vulture = "^2.10"
safety = "^2.4.0b2"
xenon = "^0.9.1"
radon = "^6.0.1"
pre-commit = "^3.6.2"
tomli = "^2.0.1"
"""

        with open(temp_dir / "pyproject.toml", "w", encoding="utf-8") as f:
            f.write(pyproject_content)

        # 配置 Poetry 使用清华源
        print("[INFO] 配置 Poetry 源...")
        run_command("poetry source remove tuna", cwd=temp_dir, retry=1)
        run_command(
            "poetry source add tuna https://pypi.tuna.tsinghua.edu.cn/simple/ --priority primary",
            cwd=temp_dir,
            retry=1,
        )

        # 安装依赖
        print("[INFO] 下载依赖到缓存...")
        code, out, err = run_command(
            "poetry install --no-root",
            cwd=temp_dir,
            retry=3,
            timeout=600,  # 增加超时时间
        )

        if code != 0:
            print("[ERROR] 依赖缓存失败")
            if err:
                print(f"[ERROR] 错误信息:\n{err}")
            return False

        # 检查缓存目录
        if cache_dir.exists():
            print("\n[INFO] 缓存目录内容:")
            for pkg in cache_dir.glob("*/*.whl"):
                print(f"  - {pkg.name}")

            print(f"\n[SUCCESS] 依赖已缓存到: {cache_dir}")
            return True
        else:
            print(f"[ERROR] 缓存目录不存在: {cache_dir}")
            return False

    except Exception as e:
        print(f"[ERROR] 缓存过程出错: {e}")
        return False
    finally:
        # 清理临时目录
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
                print("[DEBUG] 临时目录已清理")
            except Exception as e:
                print(f"[WARN] 清理临时目录失败: {e}")


def main() -> int:
    """主函数"""
    try:
        start_time = time.time()

        # 设置输出编码
        if sys.platform == "win32":
            print("[DEBUG] 配置 Windows 编码...")
            import codecs

            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
            sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)
            os.environ["PYTHONIOENCODING"] = "utf-8"
            os.environ["PYTHONUTF8"] = "1"
            # 设置控制台代码页
            os.system("chcp 65001 > NUL")

        parser = argparse.ArgumentParser(description="Python项目创建工具")
        parser.add_argument("project_name", help="项目名称", nargs="?")
        parser.add_argument(
            "--output-dir",
            type=Path,
            default=Path.home() / "projects",
            help="项目输出目录 (默认: ~/projects)",
        )
        parser.add_argument(
            "--no-cache", action="store_true", help="不使用缓存，始终从网络获取最新内容"
        )
        parser.add_argument("--cache-deps", action="store_true", help="预缓存项目依赖")
        parser.add_argument(
            "--timeout", type=int, default=300, help="命令执行超时时间（秒）"
        )
        parser.add_argument("--debug", action="store_true", help="启用详细调试输出")

        args = parser.parse_args()

        # 如果指定了预缓存，执行预缓存后退出
        if args.cache_deps:
            return 0 if cache_dependencies() else 1

        # 检查必要参数
        if not args.project_name:
            parser.error("project_name 是必需的，除非使用 --cache-deps")

        print(f"[DEBUG] 项目名称: {args.project_name}")
        print(f"[DEBUG] 输出目录: {args.output_dir}")
        print(f"[DEBUG] 使用缓存: {not args.no_cache}")
        print(f"[DEBUG] 超时时间: {args.timeout}秒")
        print(f"[DEBUG] 调试模式: {args.debug}")

        if args.debug:
            print("\n[DEBUG] 系统信息:")
            print(f"  Python版本: {sys.version}")
            print(f"  操作系统: {platform.platform()}")
            print(f"  工作目录: {os.getcwd()}")
            print(f"  环境变量: PYTHONPATH={os.environ.get('PYTHONPATH', '未设置')}")

        # 检查必要工具
        if not check_prerequisites():
            print("\n[ERROR] 请先安装所需工具后重试")
            return 1

        # 配置 Poetry 镜像源
        setup_poetry_source()

        # 创建项目
        project_dir = create_project(
            args.project_name, args.output_dir, use_cache=not args.no_cache
        )
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

    except KeyboardInterrupt:
        print("\n[INFO] 用户中断执行")
        return 130
    except Exception as e:
        print(f"\n[ERROR] 发生未预期的错误: {str(e)}")
        # 检查args是否存在且有debug属性
        if hasattr(args, "debug") and args.debug:
            import traceback

            print("\n[DEBUG] 错误堆栈:")
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
