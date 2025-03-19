#!/usr/bin/env python3
"""代码质量检查脚本。

此脚本根据配置文件运行不同级别的代码质量检查，并生成报告。
不会自动修复发现的问题。
"""

import argparse
import subprocess
import sys
import tomli
from pathlib import Path
from typing import Dict, List, Optional


class QualityChecker:
    """代码质量检查器。"""

    def __init__(self, level: str) -> None:
        """初始化检查器。

        Args:
            level: 检查级别 ('basic', 'standard', 'advanced')
        """
        self.level = level
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载对应级别的配置文件。"""
        config_file = (
            Path(__file__).parent.parent
            / "quality_checks"
            / f"{self.level}_checks.toml"
        )
        with open(config_file, "rb") as f:
            return tomli.load(f)

    def _run_command(self, cmd: List[str], tool_name: str) -> bool:
        """运行检查命令并返回是否成功。"""
        print(f"\n运行 {tool_name} 检查...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"{tool_name} 检查发现问题:")
                print(result.stdout)
                print(result.stderr)
                return False
            print(f"{tool_name} 检查通过")
            return True
        except Exception as e:
            print(f"{tool_name} 检查失败: {e}")
            return False

    def run_black_check(self) -> bool:
        """运行Black格式检查。"""
        if not self.config["black"]["enabled"]:
            return True

        cmd = [
            "poetry",
            "run",
            "black",
            "--check",
            "--line-length",
            str(self.config["black"]["line-length"]),
            ".",
        ]
        return self._run_command(cmd, "Black")

    def run_isort_check(self) -> bool:
        """运行isort导入顺序检查。"""
        if not self.config["isort"]["enabled"]:
            return True

        cmd = [
            "poetry",
            "run",
            "isort",
            "--check-only",
            "--line-length",
            str(self.config["isort"]["line-length"]),
            ".",
        ]
        return self._run_command(cmd, "isort")

    def run_ruff_check(self) -> bool:
        """运行Ruff代码检查。"""
        if not self.config["ruff"]["enabled"]:
            return True

        cmd = [
            "poetry",
            "run",
            "ruff",
            "check",
            "--select",
            ",".join(self.config["ruff"]["select"]),
            ".",
        ]
        return self._run_command(cmd, "Ruff")

    def run_mypy_check(self) -> bool:
        """运行MyPy类型检查。"""
        if not self.config["mypy"]["enabled"]:
            return True

        cmd = ["poetry", "run", "mypy", "."]
        return self._run_command(cmd, "MyPy")

    def run_pytest(self) -> bool:
        """运行PyTest测试。"""
        if not self.config["pytest"]["enabled"]:
            return True

        cmd = ["poetry", "run", "pytest"] + self.config["pytest"]["addopts"].split()
        return self._run_command(cmd, "PyTest")

    def run_additional_checks(self) -> bool:
        """运行额外的检查（标准和高级级别）。"""
        success = True

        if self.level in ["standard", "advanced"]:
            # 运行Pylint
            if self.config.get("pylint", {}).get("enabled"):
                cmd = ["poetry", "run", "pylint", "src", "tests"]
                success &= self._run_command(cmd, "Pylint")

            # 运行Bandit
            if self.config.get("bandit", {}).get("enabled"):
                cmd = ["poetry", "run", "bandit", "-r", "src"]
                success &= self._run_command(cmd, "Bandit")

            # 运行Vulture
            if self.config.get("vulture", {}).get("enabled"):
                cmd = ["poetry", "run", "vulture", "src"]
                success &= self._run_command(cmd, "Vulture")

        if self.level == "advanced":
            # 运行Safety
            if self.config.get("safety", {}).get("enabled"):
                cmd = ["poetry", "run", "safety", "check"]
                success &= self._run_command(cmd, "Safety")

            # 运行Xenon
            if self.config.get("xenon", {}).get("enabled"):
                cmd = ["poetry", "run", "xenon", "--max-absolute", "A", "src"]
                success &= self._run_command(cmd, "Xenon")

            # 运行Radon
            if self.config.get("radon", {}).get("enabled"):
                cmd = ["poetry", "run", "radon", "cc", "src"]
                success &= self._run_command(cmd, "Radon")

            # 运行Pytype
            if self.config.get("pytype", {}).get("enabled"):
                cmd = ["poetry", "run", "pytype", "src"]
                success &= self._run_command(cmd, "Pytype")

        return success

    def run_all_checks(self) -> bool:
        """运行所有启用的检查。"""
        print(f"\n开始运行{self.level}级别的代码质量检查...")

        success = True
        success &= self.run_black_check()
        success &= self.run_isort_check()
        success &= self.run_ruff_check()
        success &= self.run_mypy_check()
        success &= self.run_pytest()
        success &= self.run_additional_checks()

        if success:
            print(f"\n✅ 所有{self.level}级别的检查都通过了！")
        else:
            print(f"\n❌ {self.level}级别的某些检查未通过。请查看上面的错误信息。")

        return success


def main() -> None:
    """主函数。"""
    parser = argparse.ArgumentParser(description="运行代码质量检查")
    parser.add_argument(
        "--level",
        choices=["basic", "standard", "advanced"],
        default="basic",
        help="检查级别 (默认: basic)",
    )
    args = parser.parse_args()

    checker = QualityChecker(args.level)
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
