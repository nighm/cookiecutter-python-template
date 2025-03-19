"""命令执行相关的工具函数。"""
import subprocess
import time
from pathlib import Path
from typing import Optional, Tuple

from tqdm import tqdm


def run_command(
    command: str,
    cwd: Optional[Path] = None,
    retry: int = 3,
    timeout: int = 300
) -> Tuple[int, str, str]:
    """
    执行命令并返回结果。

    Args:
        command: 要执行的命令
        cwd: 工作目录
        retry: 重试次数
        timeout: 超时时间（秒）

    Returns:
        (返回码, 标准输出, 错误输出)
    """
    print(f"[DEBUG] 执行命令: {command}")
    if cwd:
        print(f"[DEBUG] 工作目录: {cwd}")
    print(f"[DEBUG] 超时设置: {timeout}秒")

    current_try = 1
    start_time = time.time()
    pbar = tqdm(total=100, desc="执行命令", unit="%")

    while current_try <= retry:
        try:
            if current_try > 1:
                print(f"[DEBUG] 第 {current_try} 次尝试...")

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                text=True,
                encoding="utf-8"
            )

            while process.poll() is None:
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    process.kill()
                    return 1, "", f"命令执行超时 ({timeout}秒)"
                
                progress = min(100, (elapsed / timeout) * 100)
                pbar.update(progress - pbar.n)
                time.sleep(0.1)

            stdout, stderr = process.communicate()
            code = process.returncode

            if code == 0 or "already exists" in stderr:
                print(f"[DEBUG] 命令返回码: {code}")
                if stdout:
                    print(f"[DEBUG] 标准输出:\n{stdout}")
                if stderr:
                    print(f"[DEBUG] 错误输出:\n{stderr}")
                return code, stdout, stderr

            if "network" in stderr.lower() or "timeout" in stderr.lower():
                print(f"[WARN] 网络错误，{current_try}/{retry} 次重试...")
                current_try += 1
                continue

            print(f"[DEBUG] 命令返回码: {code}")
            if stdout:
                print(f"[DEBUG] 标准输出:\n{stdout}")
            if stderr:
                print(f"[DEBUG] 错误输出:\n{stderr}")
            return code, stdout, stderr

        except Exception as e:
            print(f"[ERROR] 命令执行出错: {e}")
            return 1, "", str(e)
        finally:
            pbar.close()

    return 1, "", "超过最大重试次数" 