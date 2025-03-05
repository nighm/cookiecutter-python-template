"""健康检查模块."""
from typing import Dict, List, Optional

from pydantic import BaseModel

from src.core.cache import cache
from src.core.database import db
from src.utils.logging import get_logger

logger = get_logger(__name__)


class HealthStatus(BaseModel):
    """健康状态模型."""

    status: str
    version: str
    checks: Dict[str, bool]
    details: Optional[Dict[str, str]] = None


class HealthCheck:
    """健康检查类."""

    def __init__(self) -> None:
        """初始化健康检查."""
        self._version = "0.1.0"
        self._checks: List[str] = []

    def add_check(self, name: str) -> None:
        """添加检查项.

        Args:
            name: 检查项名称
        """
        self._checks.append(name)

    def check_health(self) -> HealthStatus:
        """基础健康检查.

        Returns:
            健康状态信息
        """
        checks = {check: True for check in self._checks}
        return HealthStatus(
            status="healthy",
            version=self._version,
            checks=checks
        )

    def check_liveness(self) -> HealthStatus:
        """Kubernetes存活检查.

        Returns:
            存活状态信息
        """
        return HealthStatus(
            status="alive",
            version=self._version,
            checks={"process": True}
        )

    async def check_readiness(self) -> HealthStatus:
        """Kubernetes就绪检查.

        Returns:
            就绪状态信息
        """
        db_status = await db.check_connection()
        cache_status = await cache.check_connection()
        storage_status = await self._check_storage()

        checks = {
            "database": db_status,
            "cache": cache_status,
            "storage": storage_status
        }

        details = {}
        if not db_status:
            details["database"] = "数据库连接失败"
        if not cache_status:
            details["cache"] = "缓存连接失败"
        if not storage_status:
            details["storage"] = "存储服务不可用"

        status = "ready" if all(checks.values()) else "not_ready"
        
        return HealthStatus(
            status=status,
            version=self._version,
            checks=checks,
            details=details if details else None
        )

    async def _check_storage(self) -> bool:
        """检查存储服务.

        Returns:
            存储是否可用
        """
        # TODO: 实现存储服务检查
        return True
