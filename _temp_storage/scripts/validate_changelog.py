#!/usr/bin/env python
import re
from pathlib import Path
from typing import List, Dict, Optional
import sys

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


def validate_semantic_version(version: str) -> bool:
    """验证版本号是否符合语义化版本规范"""
    pattern = r"^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    return bool(re.match(pattern, version))


def validate_changelog_format(content: str) -> List[str]:
    """验证变更日志格式，返回错误信息列表"""
    errors = []
    lines = content.split("\n")
    current_version = None
    current_type = None

    for i, line in enumerate(lines, 1):
        # 检查版本号格式
        if line.startswith("## ["):
            version = line.split("[")[1].split("]")[0]
            if version != "未发布" and not validate_semantic_version(version):
                errors.append(f'第{i}行: 版本号 "{version}" 不符合语义化版本规范')
            current_version = version
            current_type = None
            continue

        # 检查变更类型
        if line.startswith("### "):
            change_type = line[4:].strip()
            if change_type not in CHANGE_TYPES:
                errors.append(f'第{i}行: 未知的变更类型 "{change_type}"')
            current_type = change_type
            continue

        # 检查变更项格式
        if line.strip().startswith("- ") and current_type:
            # 检查是否包含issue引用
            if not re.search(r"\(#\d+\)", line):
                errors.append(f"第{i}行: 缺少Issue引用")

            # 检查子项格式
            next_line_idx = i
            found_subtypes = set()
            while next_line_idx < len(lines) and lines[
                next_line_idx
            ].strip().startswith("  -"):
                subtype = lines[next_line_idx].strip()[3:].split("：")[0]
                found_subtypes.add(subtype)
                next_line_idx += 1

            if current_type in CHANGE_TYPES:
                missing_subtypes = set(CHANGE_TYPES[current_type]) - found_subtypes
                if missing_subtypes:
                    errors.append(f"第{i}行: 缺少必要的子项说明: {missing_subtypes}")

    return errors


def main():
    """主函数"""
    if not CHANGELOG_PATH.exists():
        print(f"错误：找不到文件 {CHANGELOG_PATH}")
        sys.exit(1)

    content = CHANGELOG_PATH.read_text("utf-8")
    errors = validate_changelog_format(content)

    if errors:
        print("发现以下格式错误：")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    else:
        print("变更日志格式验证通过")
        sys.exit(0)


if __name__ == "__main__":
    main()
