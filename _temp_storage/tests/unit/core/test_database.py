"""数据库管理模块测试."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import DatabaseManager


@pytest.fixture
async def db_manager() -> DatabaseManager:
    """创建数据库管理器实例."""
    manager = DatabaseManager()
    yield manager
    await manager.disconnect()


async def test_database_connection(db_manager: DatabaseManager) -> None:
    """测试数据库连接."""
    # 测试连接
    await db_manager.connect()
    assert db_manager._engine is not None
    assert db_manager._session_factory is not None

    # 测试断开连接
    await db_manager.disconnect()
    assert db_manager._engine is None
    assert db_manager._session_factory is None


async def test_database_session(db_manager: DatabaseManager) -> None:
    """测试数据库会话."""
    async with db_manager.session() as session:
        assert isinstance(session, AsyncSession)
        # 测试会话可以执行查询
        result = await session.execute("SELECT 1")
        assert result.scalar() == 1


async def test_connection_check(db_manager: DatabaseManager) -> None:
    """测试连接检查."""
    # 测试未连接时的检查
    assert db_manager._engine is None
    status = await db_manager.check_connection()
    assert status is True
    assert db_manager._engine is not None

    # 测试已连接时的检查
    status = await db_manager.check_connection()
    assert status is True


async def test_session_rollback(db_manager: DatabaseManager) -> None:
    """测试会话回滚."""
    with pytest.raises(Exception):
        async with db_manager.session() as session:
            await session.execute("SELECT * FROM non_existent_table")

    # 确保可以继续使用新会话
    async with db_manager.session() as session:
        result = await session.execute("SELECT 1")
        assert result.scalar() == 1
