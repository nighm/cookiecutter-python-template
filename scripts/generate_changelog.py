#!/usr/bin/env python
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

CHANGELOG_PATH = Path(__file__).parent.parent / "CHANGELOG.md"

CHANGE_TYPES = {
    "新增": ["影响范围", "依赖要求", "性能影响"],
    "变更": ["Breaking Changes", "迁移说明", "性能影响"],
    "弃用": ["替代方案", "时间计划"],
    "移除": ["影响评估", "迁移指南"],
    "修复": ["问题描述", "修复方案", "影响范围"],
    "安全": ["漏洞等级", "CVE编号", "修复方案", "影响评估"],
    "性能": ["优化指标", "测试环境", "影响范围"],
    "文档": ["更新范围", "相关模块"],
    "依赖": ["版本变化", "兼容性", "安全影响"],
    "工程": ["工具链", "流程优化", "规范调整"],
    "测试": ["测试范围", "覆盖率", "自动化"],
}


def get_commit_messages(since_tag: Optional[str] = None) -> List[str]:
    """获取git提交信息"""
    import subprocess

    cmd = ["git", "log", "--pretty=format:%s"]
    if since_tag:
        cmd.append(f"{since_tag}..HEAD")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.splitlines()


def parse_conventional_commit(message: str) -> Dict[str, str]:
    """解析约定式提交信息"""
    pattern = r"^(feat|fix|docs|style|refactor|perf|test|chore)(\(.*\))?: (.+)$"
    if match := re.match(pattern, message):
        type_, scope, desc = match.groups()
        type_map = {
            "feat": "新增",
            "fix": "修复",
            "docs": "文档",
            "style": "工程",
            "refactor": "变更",
            "perf": "性能",
            "test": "测试",
            "chore": "工程",
        }
        return {
            "type": type_map.get(type_, type_),
            "scope": scope[1:-1] if scope else "",
            "description": desc,
        }
    return {}


def generate_changelog_entry(commits: List[str], version: str) -> str:
    """生成变更日志条目"""
    changes: Dict[str, List[Dict]] = {}
    for commit in commits:
        parsed = parse_conventional_commit(commit)
        if parsed:
            type_ = parsed["type"]
            if type_ not in changes:
                changes[type_] = []
            changes[type_].append(parsed)

    entry = [f'## [{version}] - {datetime.now().strftime("%Y-%m-%d")}\n']
    for type_ in CHANGE_TYPES:
        if type_ in changes:
            entry.append(f"### {type_}\n")
            for change in changes[type_]:
                scope = f'({change["scope"]}) ' if change["scope"] else ""
                entry.append(f'- {scope}{change["description"]}\n')
                # 添加默认的子项说明
                for subtype in CHANGE_TYPES[type_]:
                    entry.append(f"  - {subtype}：待补充\n")
            entry.append("\n")

    return "".join(entry)


def update_changelog(new_version: str):
    """更新变更日志文件"""
    if not CHANGELOG_PATH.exists():
        print(f"错误：找不到文件 {CHANGELOG_PATH}")
        sys.exit(1)

    content = CHANGELOG_PATH.read_text("utf-8")
    lines = content.splitlines()

    # 查找未发布部分的开始位置
    unreleased_start = -1
    for i, line in enumerate(lines):
        if line.startswith("## [未发布]"):
            unreleased_start = i
            break

    if unreleased_start == -1:
        print("错误：找不到未发布部分")
        sys.exit(1)

    # 获取未发布部分的内容
    unreleased_end = unreleased_start + 1
    while unreleased_end < len(lines) and not lines[unreleased_end].startswith("## ["):
        unreleased_end += 1

    # 生成新版本的变更日志
    new_entry = generate_changelog_entry(get_commit_messages(), new_version)

    # 更新文件内容
    new_content = "\n".join(lines[:unreleased_start])
    new_content += "\n## [未发布]\n\n"
    new_content += new_entry
    new_content += "\n".join(lines[unreleased_end:])

    CHANGELOG_PATH.write_text(new_content, "utf-8")
    print(f"已更新变更日志到版本 {new_version}")


def main():
    if len(sys.argv) != 2:
        print("用法：python generate_changelog.py <new_version>")
        sys.exit(1)

    new_version = sys.argv[1]
    update_changelog(new_version)


if __name__ == "__main__":
    main()
