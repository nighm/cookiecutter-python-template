"""日志配置和工具.

提供结构化日志记录的配置和实用工具。
"""

import logging.config
import sys
from typing import Any, Dict, Optional

import structlog
from structlog.types import Processor

from src.config import settings


def configure_logging() -> None:
    """配置应用程序的结构化日志系统.

    配置包括:
    - 日志格式化
    - 时间戳格式
    - 错误堆栈信息
    - JSON或控制台输出
    """
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,  # 合并上下文变量
        structlog.processors.add_log_level,  # 添加日志级别
        structlog.processors.TimeStamper(fmt="iso"),  # ISO格式时间戳
        structlog.processors.StackInfoRenderer(),  # 堆栈信息
        structlog.processors.format_exc_info,  # 异常信息格式化
    ]

    # 根据配置选择JSON或控制台输出格式
    if settings.LOG_FORMAT.lower() == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.LOG_LEVEL)
        ),
        cache_logger_on_first_use=True,
    )


def get_logger(name: Optional[str] = None) -> structlog.BoundLogger:
    """获取日志记录器实例.

    Args:
        name: 日志记录器名称，可选

    Returns:
        配置好的日志记录器实例
    """
    return structlog.get_logger(name)
