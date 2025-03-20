"""监控模块."""
from src.monitoring.health import HealthCheck
from src.monitoring.metrics import metrics

# 创建全局健康检查实例
health = HealthCheck()

__all__ = ["health", "metrics"]
