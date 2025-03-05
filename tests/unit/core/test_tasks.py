"""任务管理模块测试."""
import asyncio
from datetime import datetime, timedelta

import pytest
from apscheduler.triggers.cron import CronTrigger

from src.core.tasks import TaskManager


@pytest.fixture
def task_manager() -> TaskManager:
    """创建任务管理器实例."""
    return TaskManager()


async def test_background_task(task_manager: TaskManager) -> None:
    """测试后台任务."""
    test_result = []

    @task_manager.background_task(name="test_task")
    async def test_task() -> None:
        test_result.append(1)
        await asyncio.sleep(0.1)
        test_result.append(2)

    # 运行任务
    await test_task()
    assert test_result == [1, 2]


async def test_background_task_retry(task_manager: TaskManager) -> None:
    """测试后台任务重试."""
    retry_count = 0

    @task_manager.background_task(name="retry_task", max_retries=2, retry_delay=0)
    async def retry_task() -> None:
        nonlocal retry_count
        retry_count += 1
        raise ValueError("Test error")

    # 运行任务，应该重试两次
    with pytest.raises(ValueError):
        await retry_task()
    assert retry_count == 3  # 初始运行 + 2次重试


async def test_schedule_task(task_manager: TaskManager) -> None:
    """测试定时任务."""
    run_count = 0

    @task_manager.schedule_task(cron="* * * * *", name="test_schedule")
    async def scheduled_task() -> None:
        nonlocal run_count
        run_count += 1

    # 获取任务列表
    tasks = task_manager.get_active_tasks()
    assert len(tasks) == 1
    assert tasks[0]["name"] == "test_schedule"
    assert tasks[0]["type"] == "scheduled"


async def test_get_active_tasks(task_manager: TaskManager) -> None:
    """测试获取活动任务列表."""
    # 添加后台任务
    @task_manager.background_task(name="bg_task")
    async def bg_task() -> None:
        await asyncio.sleep(0.1)

    # 添加定时任务
    @task_manager.schedule_task(cron="0 * * * *", name="scheduled_task")
    async def scheduled_task() -> None:
        pass

    # 启动后台任务
    asyncio.create_task(bg_task())

    # 获取任务列表
    tasks = task_manager.get_active_tasks()
    assert len(tasks) == 2

    bg_task_info = next(t for t in tasks if t["name"] == "bg_task")
    assert bg_task_info["type"] == "background"

    scheduled_task_info = next(t for t in tasks if t["name"] == "scheduled_task")
    assert scheduled_task_info["type"] == "scheduled"


async def test_cancel_task(task_manager: TaskManager) -> None:
    """测试取消任务."""
    # 添加后台任务
    @task_manager.background_task(name="cancel_test")
    async def long_task() -> None:
        await asyncio.sleep(10)

    # 启动任务
    asyncio.create_task(long_task())

    # 取消任务
    result = await task_manager.cancel_task("cancel_test")
    assert result is True

    # 尝试取消不存在的任务
    result = await task_manager.cancel_task("non_existent")
    assert result is False


def test_cron_trigger_validation(task_manager: TaskManager) -> None:
    """测试Cron表达式验证."""
    # 有效的Cron表达式
    trigger = CronTrigger.from_crontab("*/5 * * * *")
    next_run = trigger.get_next_fire_time(
        None,
        datetime.now()
    )
    assert next_run is not None
    
    # 无效的Cron表达式
    with pytest.raises(ValueError):
        CronTrigger.from_crontab("invalid cron")
