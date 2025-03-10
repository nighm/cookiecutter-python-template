"""数据库连接管理模块."""
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """数据库管理器."""

    def __init__(self) -> None:
        """初始化数据库管理器."""
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[sessionmaker] = None

    async def connect(self) -> None:
        """建立数据库连接."""
        if self._engine is not None:
            return

        self._engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.SQL_DEBUG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
        )

        self._session_factory = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        logger.info("Database connection established")

    async def disconnect(self) -> None:
        """关闭数据库连接."""
        if self._engine is None:
            return

        await self._engine.dispose()
        self._engine = None
        self._session_factory = None
        logger.info("Database connection closed")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """创建数据库会话.

        Yields:
            数据库会话
        """
        if self._session_factory is None:
            await self.connect()

        async with self._session_factory() as session:  # type: ignore
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def check_connection(self) -> bool:
        """检查数据库连接状态.

        Returns:
            连接是否正常
        """
        try:
            if self._engine is None:
                await self.connect()

            async with self._engine.connect() as conn:  # type: ignore
                await conn.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error("Database connection check failed", exc_info=e)
            return False


# 全局数据库管理器实例
db = DatabaseManager()
