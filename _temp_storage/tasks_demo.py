"""任务示例模块."""
import asyncio
from datetime import datetime
from typing import List

from src.core.cache import cache
from src.core.tasks import task_manager
from src.utils.logging import get_logger

logger = get_logger(__name__)


@task_manager.background_task(name="data_processor", max_retries=3)
async def process_data(items: List[str]) -> None:
    """处理数据的后台任务.

    Args:
        items: 要处理的数据项
    """
    logger.info(f"开始处理 {len(items)} 条数据")
    for item in items:
        # 模拟处理时间
        await asyncio.sleep(1)
        logger.info(f"处理数据: {item}")
    logger.info("数据处理完成")


@task_manager.background_task(name="cache_cleaner")
async def clean_expired_cache() -> None:
    """清理过期缓存的后台任务."""
    logger.info("开始清理过期缓存")
    # 模拟清理操作
    await asyncio.sleep(2)
    logger.info("缓存清理完成")


@task_manager.schedule_task(cron="*/5 * * * *", name="stats_collector")
async def collect_stats() -> None:
    """每5分钟收集统计数据的定时任务."""
    logger.info("开始收集统计数据")
    try:
        # 收集一些示例统计数据
        stats = {
            "timestamp": datetime.now().isoformat(),
            "active_tasks": len(task_manager.get_active_tasks()),
            "memory_usage": "128MB",  # 示例值
            "cpu_usage": "25%"  # 示例值
        }
        # 保存到缓存
        await cache.set(
            f"stats:{stats['timestamp']}",
            str(stats),
            expire=3600  # 1小时过期
        )
        logger.info("统计数据收集完成")
    except Exception as e:
        logger.error("统计数据收集失败", exc_info=e)


@task_manager.schedule_task(cron="0 0 * * *", name="daily_backup")
async def daily_backup() -> None:
    """每天凌晨执行备份的定时任务."""
    logger.info("开始执行每日备份")
    try:
        # 模拟备份操作
        await asyncio.sleep(5)
        logger.info("备份完成")
    except Exception as e:
        logger.error("备份失败", exc_info=e)


async def run_task_demo() -> None:
    """运行任务示例."""
    # 启动后台任务
    await process_data(["item1", "item2", "item3"])
    await clean_expired_cache()

    # 查看活动任务
    tasks = task_manager.get_active_tasks()
    logger.info(f"活动任务: {tasks}")

    # 等待一段时间以便观察定时任务
    logger.info("等待定时任务执行...")
    await asyncio.sleep(10)

    # 取消一个任务
    await task_manager.cancel_task("stats_collector")
    logger.info("已取消统计数据收集任务")


if __name__ == "__main__":
    asyncio.run(run_task_demo())
