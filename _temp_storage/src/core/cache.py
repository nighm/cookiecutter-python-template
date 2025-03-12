"""缓存管理模块."""
from typing import Any, Optional

import aioredis
from aioredis import Redis

from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class CacheManager:
    """缓存管理器."""

    def __init__(self) -> None:
        """初始化缓存管理器."""
        self._redis: Optional[Redis] = None

    async def connect(self) -> None:
        """建立Redis连接."""
        if self._redis is not None:
            return

        self._redis = await aioredis.create_redis_pool(
            settings.REDIS_URL,
            minsize=settings.REDIS_POOL_MIN_SIZE,
            maxsize=settings.REDIS_POOL_MAX_SIZE,
            encoding="utf-8",
        )
        logger.info("Redis connection established")

    async def disconnect(self) -> None:
        """关闭Redis连接."""
        if self._redis is None:
            return

        self._redis.close()
        await self._redis.wait_closed()
        self._redis = None
        logger.info("Redis connection closed")

    async def get(self, key: str) -> Any:
        """获取缓存值.

        Args:
            key: 缓存键

        Returns:
            缓存值
        """
        if self._redis is None:
            await self.connect()
        return await self._redis.get(key)  # type: ignore

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        """设置缓存值.

        Args:
            key: 缓存键
            value: 缓存值
            expire: 过期时间（秒）
        """
        if self._redis is None:
            await self.connect()
        await self._redis.set(key, value, expire=expire)  # type: ignore

    async def delete(self, key: str) -> None:
        """删除缓存值.

        Args:
            key: 缓存键
        """
        if self._redis is None:
            await self.connect()
        await self._redis.delete(key)  # type: ignore

    async def check_connection(self) -> bool:
        """检查Redis连接状态.

        Returns:
            连接是否正常
        """
        try:
            if self._redis is None:
                await self.connect()
            await self._redis.ping()  # type: ignore
            return True
        except Exception as e:
            logger.error("Redis connection check failed", exc_info=e)
            return False


# 全局缓存管理器实例
cache = CacheManager()
