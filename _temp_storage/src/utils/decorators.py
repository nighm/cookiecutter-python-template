"""项目通用装饰器.

提供常用的功能装饰器，如重试、计时和废弃标记等。
"""

import functools
import time
from typing import Any, Callable, TypeVar, cast

from src.utils.logging import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """函数调用失败重试装饰器.

    Args:
        max_attempts: 最大重试次数
        delay: 重试间隔时间（秒）
        backoff_factor: 重试间隔时间的增长因子
        exceptions: 需要捕获的异常类型

    Returns:
        装饰后的函数
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        raise

                    logger.warning(
                        "函数调用失败",
                        function=func.__name__,
                        attempt=attempt + 1,
                        max_attempts=max_attempts,
                        error=str(e),
                    )

                    time.sleep(current_delay)
                    current_delay *= backoff_factor

            if last_exception:
                raise last_exception
            return None

        return cast(F, wrapper)

    return decorator


def timing(func: F) -> F:
    """测量函数执行时间的装饰器.

    Args:
        func: 需要测量时间的函数

    Returns:
        装饰后的函数
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.debug(
            "函数执行时间",
            function=func.__name__,
            duration_seconds=duration,
        )
        return result

    return cast(F, wrapper)


def deprecated(func: F) -> F:
    """标记函数为已废弃的装饰器.

    Args:
        func: 需要标记为废弃的函数

    Returns:
        装饰后的函数
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.warning(
            "调用了已废弃的函数",
            function=func.__name__,
        )
        return func(*args, **kwargs)

    return cast(F, wrapper)
