"""指标监控模块."""
from typing import Dict, List, Optional, Union

from prometheus_client import Counter, Gauge, Histogram, Summary


class MetricsManager:
    """指标管理类."""

    def __init__(self) -> None:
        """初始化指标管理器."""
        self._metrics: Dict[str, Union[Counter, Gauge, Histogram, Summary]] = {}

    def counter(
        self, name: str, description: str, labels: Optional[List[str]] = None
    ) -> Counter:
        """创建计数器指标.

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签列表

        Returns:
            计数器指标对象
        """
        if name not in self._metrics:
            self._metrics[name] = Counter(name, description, labels or [])
        return self._metrics[name]  # type: ignore

    def gauge(
        self, name: str, description: str, labels: Optional[List[str]] = None
    ) -> Gauge:
        """创建仪表盘指标.

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签列表

        Returns:
            仪表盘指标对象
        """
        if name not in self._metrics:
            self._metrics[name] = Gauge(name, description, labels or [])
        return self._metrics[name]  # type: ignore

    def histogram(
        self,
        name: str,
        description: str,
        labels: Optional[List[str]] = None,
        buckets: Optional[List[float]] = None,
    ) -> Histogram:
        """创建直方图指标.

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签列表
            buckets: 直方图桶

        Returns:
            直方图指标对象
        """
        if name not in self._metrics:
            self._metrics[name] = Histogram(
                name, description, labels or [], buckets=buckets
            )
        return self._metrics[name]  # type: ignore

    def summary(
        self, name: str, description: str, labels: Optional[List[str]] = None
    ) -> Summary:
        """创建摘要指标.

        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签列表

        Returns:
            摘要指标对象
        """
        if name not in self._metrics:
            self._metrics[name] = Summary(name, description, labels or [])
        return self._metrics[name]  # type: ignore


# 全局指标管理器实例
metrics = MetricsManager()
