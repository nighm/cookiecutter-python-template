"""高级级别检查的测试示例。

这个模块展示了高级级别检查会关注的代码质量问题，包括：
1. 安全性检查
2. 性能优化
3. 并发处理
4. 资源管理
5. 高级类型检查
"""
import asyncio
import contextlib
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import (
    AsyncIterator,
    Callable,
    ContextManager,
    Dict,
    Generic,
    List,
    Optional,
    TypeVar,
    Union,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class ResourceManager(Generic[T]):
    """资源管理器，展示高级级别的代码质量要求。

    这个类展示了：
    1. 泛型使用
    2. 上下文管理
    3. 资源清理
    4. 线程安全
    """

    def __init__(self, resource_factory: Callable[[], T]):
        """初始化资源管理器。

        Args:
            resource_factory: 创建资源的工厂函数
        """
        self._factory = resource_factory
        self._resource: Optional[T] = None
        self._lock = asyncio.Lock()

    async def __aenter__(self) -> T:
        """异步上下文管理器入口。

        Returns:
            管理的资源对象

        Raises:
            RuntimeError: 如果资源已经在使用中
        """
        async with self._lock:
            if self._resource is not None:
                raise RuntimeError("Resource already in use")
            self._resource = self._factory()
            return self._resource

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """异步上下文管理器出口。

        Args:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常回溯
        """
        async with self._lock:
            if hasattr(self._resource, 'close'):
                await self._resource.close()
            self._resource = None


class DataProcessor:
    """高级数据处理器，展示性能优化和并发处理。"""

    def __init__(self, max_workers: int = 4):
        """初始化数据处理器。

        Args:
            max_workers: 最大工作线程数，默认为4
        """
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._cache: Dict[str, float] = {}

    @contextlib.contextmanager
    def performance_logging(self, operation: str) -> ContextManager[None]:
        """性能日志记录器。

        Args:
            operation: 操作名称

        Yields:
            上下文管理器
        """
        start_time = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            logger.info(f"{operation} took {duration:.2f} seconds")

    async def process_batch(
        self, items: List[Union[int, float]], chunk_size: int = 1000
    ) -> AsyncIterator[List[float]]:
        """异步批处理数据。

        Args:
            items: 要处理的数据项列表
            chunk_size: 每批处理的数据量，默认为1000

        Yields:
            处理后的数据批次

        Raises:
            ValueError: 如果chunk_size小于等于0
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        for i in range(0, len(items), chunk_size):
            chunk = items[i:i + chunk_size]
            with self.performance_logging(f"Processing chunk {i//chunk_size}"):
                # 使用线程池处理计算密集型任务
                results = await asyncio.get_event_loop().run_in_executor(
                    self._executor,
                    lambda: [float(x) * 2 for x in chunk]
                )
                yield results

    def __del__(self):
        """清理资源。"""
        self._executor.shutdown(wait=True)


async def test_resource_manager():
    """测试资源管理器。"""
    # 创建资源管理器
    manager = ResourceManager(list)

    # 测试异步上下文管理器
    async with manager as resource:
        assert isinstance(resource, list)
        resource.append(1)
        assert len(resource) == 1

    # 测试资源清理
    assert manager._resource is None

    # 测试并发访问
    async with asyncio.TaskGroup() as group:
        for _ in range(3):
            group.create_task(test_concurrent_access(manager))


async def test_concurrent_access(manager: ResourceManager[list]):
    """测试并发访问资源。"""
    try:
        async with manager as _:
            await asyncio.sleep(0.1)
    except RuntimeError:
        # 预期的并发访问错误
        pass


async def test_data_processor():
    """测试数据处理器。"""
    processor = DataProcessor(max_workers=2)

    # 准备测试数据
    test_data = list(range(3000))

    # 测试批处理
    batch_count = 0
    total_items = 0
    async for batch in processor.process_batch(test_data, chunk_size=1000):
        batch_count += 1
        total_items += len(batch)
        # 验证处理结果
        assert all(isinstance(x, float) for x in batch)

    assert batch_count == 3
    assert total_items == len(test_data) 