"""健康检查模块测试."""
import pytest

from src.monitoring.health import HealthCheck, HealthStatus


@pytest.fixture
def health_check() -> HealthCheck:
    """创建健康检查实例."""
    return HealthCheck()


def test_health_check_initialization(health_check: HealthCheck) -> None:
    """测试健康检查初始化."""
    assert isinstance(health_check, HealthCheck)
    assert health_check._version == "0.1.0"
    assert health_check._checks == []


def test_add_check(health_check: HealthCheck) -> None:
    """测试添加检查项."""
    health_check.add_check("test_check")
    assert "test_check" in health_check._checks


def test_check_health(health_check: HealthCheck) -> None:
    """测试基础健康检查."""
    health_check.add_check("test_check")
    status = health_check.check_health()

    assert isinstance(status, HealthStatus)
    assert status.status == "healthy"
    assert status.version == "0.1.0"
    assert status.checks == {"test_check": True}


def test_check_liveness(health_check: HealthCheck) -> None:
    """测试存活检查."""
    status = health_check.check_liveness()

    assert isinstance(status, HealthStatus)
    assert status.status == "alive"
    assert status.version == "0.1.0"
    assert status.checks == {"process": True}


def test_check_readiness(health_check: HealthCheck) -> None:
    """测试就绪检查."""
    status = health_check.check_readiness()

    assert isinstance(status, HealthStatus)
    assert status.status == "ready"
    assert status.version == "0.1.0"
    assert status.checks == {"database": True, "cache": True, "storage": True}


def test_health_status_model() -> None:
    """测试健康状态模型."""
    status = HealthStatus(
        status="healthy",
        version="0.1.0",
        checks={"test": True},
        details={"message": "All systems operational"},
    )

    assert status.status == "healthy"
    assert status.version == "0.1.0"
    assert status.checks == {"test": True}
    assert status.details == {"message": "All systems operational"}
