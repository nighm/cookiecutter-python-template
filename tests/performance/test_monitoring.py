"""监控模块性能测试."""
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

import pytest
from fastapi.testclient import TestClient

from src.examples.web_app import app
from src.monitoring import health, metrics

client = TestClient(app)


def measure_time(func: Callable) -> float:
    """测量函数执行时间.

    Args:
        func: 要测量的函数

    Returns:
        执行时间（秒）
    """
    start_time = time.time()
    func()
    return time.time() - start_time


def test_health_check_performance() -> None:
    """测试健康检查性能."""
    # 执行100次健康检查
    times = []
    for _ in range(100):
        times.append(measure_time(health.check_health))
    
    # 计算平均执行时间
    avg_time = sum(times) / len(times)
    assert avg_time < 0.001  # 确保每次检查小于1ms


def test_metrics_performance() -> None:
    """测试指标性能."""
    counter = metrics.counter("perf_test_counter", "Performance test counter")
    histogram = metrics.histogram(
        "perf_test_histogram",
        "Performance test histogram"
    )
    
    # 执行1000次指标记录
    times = []
    for _ in range(1000):
        start_time = time.time()
        counter.inc()
        histogram.observe(0.1)
        times.append(time.time() - start_time)
    
    # 计算平均执行时间
    avg_time = sum(times) / len(times)
    assert avg_time < 0.0001  # 确保每次记录小于0.1ms


def test_concurrent_health_checks() -> None:
    """测试并发健康检查."""
    def check_health() -> None:
        response = client.get("/health")
        assert response.status_code == 200

    # 使用10个线程并发执行100次健康检查
    with ThreadPoolExecutor(max_workers=10) as executor:
        start_time = time.time()
        list(executor.map(lambda _: check_health(), range(100)))
        total_time = time.time() - start_time
    
    # 确保总执行时间在合理范围内
    assert total_time < 2  # 所有请求应在2秒内完成


def test_metrics_endpoint_performance() -> None:
    """测试指标端点性能."""
    # 生成一些测试数据
    for _ in range(100):
        client.get("/")
        client.get("/health")
    
    # 测量指标端点响应时间
    times = []
    for _ in range(10):
        times.append(measure_time(lambda: client.get("/metrics")))
    
    # 计算平均响应时间
    avg_time = sum(times) / len(times)
    assert avg_time < 0.1  # 确保指标收集小于100ms


@pytest.mark.benchmark
def test_health_check_benchmark(benchmark) -> None:
    """基准测试：健康检查."""
    benchmark(health.check_health)


@pytest.mark.benchmark
def test_metrics_benchmark(benchmark) -> None:
    """基准测试：指标记录."""
    counter = metrics.counter("bench_counter", "Benchmark counter")
    benchmark(counter.inc)
