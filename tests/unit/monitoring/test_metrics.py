"""指标监控模块测试."""
from prometheus_client import Counter, Gauge, Histogram, Summary

from src.monitoring.metrics import MetricsManager


def test_metrics_manager_initialization() -> None:
    """测试指标管理器初始化."""
    manager = MetricsManager()
    assert isinstance(manager, MetricsManager)
    assert manager._metrics == {}


def test_counter_creation() -> None:
    """测试创建计数器指标."""
    manager = MetricsManager()
    counter = manager.counter(
        "test_counter",
        "Test counter",
        ["label1", "label2"]
    )
    
    assert isinstance(counter, Counter)
    assert "test_counter" in manager._metrics


def test_counter_reuse() -> None:
    """测试重用计数器指标."""
    manager = MetricsManager()
    counter1 = manager.counter("test_counter", "Test counter")
    counter2 = manager.counter("test_counter", "Test counter")
    
    assert counter1 is counter2


def test_gauge_creation() -> None:
    """测试创建仪表盘指标."""
    manager = MetricsManager()
    gauge = manager.gauge(
        "test_gauge",
        "Test gauge",
        ["label1"]
    )
    
    assert isinstance(gauge, Gauge)
    assert "test_gauge" in manager._metrics


def test_histogram_creation() -> None:
    """测试创建直方图指标."""
    manager = MetricsManager()
    histogram = manager.histogram(
        "test_histogram",
        "Test histogram",
        ["label1"],
        buckets=[0.1, 0.5, 1.0]
    )
    
    assert isinstance(histogram, Histogram)
    assert "test_histogram" in manager._metrics


def test_summary_creation() -> None:
    """测试创建摘要指标."""
    manager = MetricsManager()
    summary = manager.summary(
        "test_summary",
        "Test summary",
        ["label1"]
    )
    
    assert isinstance(summary, Summary)
    assert "test_summary" in manager._metrics


def test_metrics_functionality() -> None:
    """测试指标功能."""
    manager = MetricsManager()
    
    # 测试计数器
    counter = manager.counter("test_counter", "Test counter", ["type"])
    counter.labels(type="test").inc()
    
    # 测试仪表盘
    gauge = manager.gauge("test_gauge", "Test gauge")
    gauge.set(42)
    
    # 测试直方图
    histogram = manager.histogram(
        "test_histogram",
        "Test histogram",
        buckets=[0.1, 1.0, 10.0]
    )
    histogram.observe(0.5)
    
    # 测试摘要
    summary = manager.summary("test_summary", "Test summary")
    summary.observe(100)
