"""任务管理模块."""
import asyncio
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, TypeVar

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.utils.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


class TaskManager:
    """任务管理器."""

    def __init__(self) -> None:
        """初始化任务管理器."""
        self._tasks: Dict[str, asyncio.Task] = {}
        self._scheduler = AsyncIOScheduler()
        self._scheduler.start()

    def background_task(
        self,
        name: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: int = 5
    ) -> Callable:
        """后台任务装饰器.

        Args:
            name: 任务名称
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）

        Returns:
            装饰器函数
        """
        def decorator(func: Callable) -> Callable:
            task_name = name or func.__name__

            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> None:
                retries = 0
                while retries <= max_retries:
                    try:
                        task = asyncio.create_task(func(*args, **kwargs))
                        self._tasks[task_name] = task
                        await task
                        break
                    except Exception as e:
                        retries += 1
                        if retries > max_retries:
                            logger.error(
                                f"Task {task_name} failed after {max_retries} retries",
                                exc_info=e
                            )
                            raise
                        logger.warning(
                            f"Task {task_name} failed, retrying in {retry_delay} seconds",
                            exc_info=e
                        )
                        await asyncio.sleep(retry_delay)
                    finally:
                        if task_name in self._tasks:
                            del self._tasks[task_name]

            return wrapper
        return decorator

    def schedule_task(
        self,
        cron: str,
        name: Optional[str] = None,
        max_instances: int = 1
    ) -> Callable:
        """定时任务装饰器.

        Args:
            cron: Cron表达式
            name: 任务名称
            max_instances: 最大并发实例数

        Returns:
            装饰器函数
        """
        def decorator(func: Callable) -> Callable:
            task_name = name or func.__name__

            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> None:
                try:
                    await func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Scheduled task {task_name} failed", exc_info=e)

            # 注册定时任务
            self._scheduler.add_job(
                wrapper,
                CronTrigger.from_crontab(cron),
                id=task_name,
                name=task_name,
                max_instances=max_instances,
                replace_existing=True
            )
            return wrapper
        return decorator

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """获取活动任务列表.

        Returns:
            活动任务列表
        """
        tasks = []
        # 后台任务
        for name, task in self._tasks.items():
            tasks.append({
                "name": name,
                "type": "background",
                "status": "running" if not task.done() else "completed",
                "created_at": task.get_coro().cr_frame.f_locals.get("start_time", "N/A")
            })
        
        # 定时任务
        for job in self._scheduler.get_jobs():
            tasks.append({
                "name": job.name,
                "type": "scheduled",
                "status": "scheduled",
                "next_run": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
                if job.next_run_time else "N/A"
            })
        
        return tasks

    async def cancel_task(self, name: str) -> bool:
        """取消任务.

        Args:
            name: 任务名称

        Returns:
            是否成功取消
        """
        # 取消后台任务
        if name in self._tasks:
            task = self._tasks[name]
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self._tasks[name]
            return True

        # 取消定时任务
        job = self._scheduler.get_job(name)
        if job:
            job.remove()
            return True

        return False


# 全局任务管理器实例
task_manager = TaskManager()
