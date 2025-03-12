#!/usr/bin/env python3
"""
检查是否需要更新README.md文件
"""

import os
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


def load_config() -> Dict:
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config" / "readme_config.yml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_changed_files() -> List[str]:
    """获取最近更改的文件列表"""
    # 如果是定时任务，返回空列表
    if os.getenv("GITHUB_EVENT_NAME") == "schedule":
        return []

    # 获取最近的commit中更改的文件
    import subprocess

    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD^", "HEAD"], capture_output=True, text=True
    )
    return result.stdout.strip().split("\n")


def should_update(config: Dict, changed_files: List[str]) -> bool:
    """判断是否需要更新README"""
    # 如果是定时任务，检查上次更新时间
    if os.getenv("GITHUB_EVENT_NAME") == "schedule":
        last_update = get_last_update_time()
        if datetime.now() - last_update >= timedelta(days=7):
            return True
        return False

    # 检查每个更新规则
    for rule_name, rule in config["update_rules"].items():
        if not rule.get("enabled", True):
            continue

        # 检查文件变更是否触发更新
        for trigger in rule["triggers"]:
            for file in changed_files:
                if Path(file).match(trigger):
                    return True

    return False


def get_last_update_time() -> datetime:
    """获取上次更新时间"""
    readme_path = Path(__file__).parent.parent.parent / "README.md"
    if not readme_path.exists():
        return datetime.min

    # 获取文件最后修改时间
    return datetime.fromtimestamp(readme_path.stat().st_mtime)


def main():
    """主函数"""
    config = load_config()
    changed_files = get_changed_files()
    update_needed = should_update(config, changed_files)

    # 设置GitHub Actions输出变量
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"should_update={str(update_needed).lower()}\n")

    # 打印调试信息
    print(f"Changed files: {changed_files}")
    print(f"Update needed: {update_needed}")


if __name__ == "__main__":
    main()
