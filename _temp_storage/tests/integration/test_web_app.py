"""Web应用集成测试."""
from fastapi.testclient import TestClient

from src.examples.web_app import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """测试根路径端点."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the example web app!"}


def test_health_check_endpoint() -> None:
    """测试健康检查端点."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_liveness_endpoint() -> None:
    """测试存活检查端点."""
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_endpoint() -> None:
    """测试就绪检查端点."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_metrics_endpoint() -> None:
    """测试指标端点."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


def test_metrics_collection() -> None:
    """测试指标收集."""
    # 发送请求以触发指标收集
    client.get("/")
    client.get("/health")

    # 检查指标是否被收集
    response = client.get("/metrics")
    assert response.status_code == 200
    metrics_text = response.text

    # 验证请求计数器
    assert 'http_requests_total{endpoint="/",method="GET",status="200"}' in metrics_text
    assert (
        'http_requests_total{endpoint="/health",method="GET",status="200"}'
        in metrics_text
    )
