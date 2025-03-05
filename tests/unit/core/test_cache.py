"""缓存管理模块测试."""
import pytest

from src.core.cache import CacheManager


@pytest.fixture
async def cache_manager() -> CacheManager:
    """创建缓存管理器实例."""
    manager = CacheManager()
    yield manager
    await manager.disconnect()


async def test_cache_connection(cache_manager: CacheManager) -> None:
    """测试缓存连接."""
    # 测试连接
    await cache_manager.connect()
    assert cache_manager._redis is not None

    # 测试断开连接
    await cache_manager.disconnect()
    assert cache_manager._redis is None


async def test_cache_operations(cache_manager: CacheManager) -> None:
    """测试缓存操作."""
    # 设置缓存
    await cache_manager.set("test_key", "test_value")
    
    # 获取缓存
    value = await cache_manager.get("test_key")
    assert value == "test_value"
    
    # 删除缓存
    await cache_manager.delete("test_key")
    value = await cache_manager.get("test_key")
    assert value is None


async def test_cache_expiration(cache_manager: CacheManager) -> None:
    """测试缓存过期."""
    # 设置带过期时间的缓存
    await cache_manager.set("test_key", "test_value", expire=1)
    
    # 立即获取
    value = await cache_manager.get("test_key")
    assert value == "test_value"
    
    # 等待过期
    import asyncio
    await asyncio.sleep(1.1)
    
    # 过期后获取
    value = await cache_manager.get("test_key")
    assert value is None


async def test_connection_check(cache_manager: CacheManager) -> None:
    """测试连接检查."""
    # 测试未连接时的检查
    assert cache_manager._redis is None
    status = await cache_manager.check_connection()
    assert status is True
    assert cache_manager._redis is not None

    # 测试已连接时的检查
    status = await cache_manager.check_connection()
    assert status is True


async def test_multiple_connections(cache_manager: CacheManager) -> None:
    """测试多次连接."""
    # 首次连接
    await cache_manager.connect()
    redis1 = cache_manager._redis

    # 再次连接（应该复用现有连接）
    await cache_manager.connect()
    redis2 = cache_manager._redis

    assert redis1 is redis2  # 确保是同一个连接
