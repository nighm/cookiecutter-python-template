"""核心功能模块。

此模块包含项目的核心功能实现。
"""

from typing import Any, Dict
import sys

__all__ = ["get_version"]


def get_version() -> Dict[str, Any]:
    """获取当前版本信息。

    Returns:
        包含版本信息的字典
    """
    from .. import __version__
    return {
        "version": __version__,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    } 