"""编码和兼容性配置.

此模块定义了项目范围的编码和兼容性设置，确保所有Python文件的一致性。
"""

import sys
from typing import NoReturn


def check_python_version() -> None:
    """检查Python版本是否满足要求."""
    min_version = (3, 8)
    if sys.version_info < min_version:
        raise RuntimeError(f"需要Python {'.'.join(map(str, min_version))} 或更高版本")


def check_encoding() -> None:
    """检查系统编码设置."""
    if sys.getdefaultencoding() != "utf-8":
        raise RuntimeError("系统默认编码必须是UTF-8")


def verify_environment() -> None:
    """验证运行环境是否满足所有要求."""
    check_python_version()
    check_encoding()


# 在导入时执行环境检查
verify_environment()
