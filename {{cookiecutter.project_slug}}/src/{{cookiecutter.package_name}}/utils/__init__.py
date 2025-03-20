"""工具模块。

此模块包含项目中使用的通用工具函数。
"""

from typing import Any, Dict, List, Optional
import json
import os
import logging
from pathlib import Path

__all__ = ["load_json", "save_json", "setup_logging"]


def load_json(file_path: str) -> Dict[str, Any]:
    """从JSON文件加载数据。

    Args:
        file_path: JSON文件路径

    Returns:
        加载的JSON数据

    Raises:
        FileNotFoundError: 文件不存在时抛出
        json.JSONDecodeError: JSON格式错误时抛出
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """保存数据到JSON文件。

    Args:
        data: 要保存的数据
        file_path: 目标文件路径

    Raises:
        OSError: 写入文件失败时抛出
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def setup_logging(
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> None:
    """设置日志配置。

    Args:
        log_file: 日志文件路径，如果为None则只输出到控制台
        level: 日志级别
        format_str: 日志格式字符串
    """
    handlers: List[logging.Handler] = [logging.StreamHandler()]
    
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))

    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=handlers
    ) 