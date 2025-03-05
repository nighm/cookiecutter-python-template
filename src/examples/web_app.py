"""示例Web应用."""
from typing import Dict

from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.monitoring import health, metrics
from src.utils.logging import get_logger

logger = get_logger(__name__)

# 创建FastAPI应用
app = FastAPI(title="示例Web应用")

# 创建指标中间件
metrics_app = make_asgi_app()

# 请求计数器
request_count = metrics.counter(
    "http_requests_total",
    "Total HTTP requests count",
    ["method", "endpoint", "status"]
)

# 请求延迟直方图
request_latency = metrics.histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """指标收集中间件."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """处理请求并收集指标.

        Args:
            request: HTTP请求
            call_next: 下一个处理器

        Returns:
            HTTP响应
        """
        try:
            response = await call_next(request)
            request_count.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            return response
        except Exception as e:
            logger.error("Request failed", exc_info=e)
            raise


# 注册中间件
app.add_middleware(MetricsMiddleware)

# 注册指标端点
app.mount("/metrics", metrics_app)


@app.get("/")
async def root() -> Dict[str, str]:
    """根路径处理器.

    Returns:
        欢迎消息
    """
    return {"message": "Welcome to the example web app!"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """健康检查端点.

    Returns:
        健康状态信息

    Raises:
        HTTPException: 当服务不健康时
    """
    status = health.check_health()
    if status.status != "healthy":
        raise HTTPException(status_code=503, detail="Service unhealthy")
    return {"status": "healthy"}


@app.get("/health/live")
async def liveness() -> Dict[str, str]:
    """存活检查端点.

    Returns:
        存活状态信息
    """
    status = health.check_liveness()
    return {"status": status.status}


@app.get("/health/ready")
async def readiness() -> Dict[str, str]:
    """就绪检查端点.

    Returns:
        就绪状态信息

    Raises:
        HTTPException: 当服务未就绪时
    """
    status = health.check_readiness()
    if status.status != "ready":
        raise HTTPException(status_code=503, detail="Service not ready")
    return {"status": "ready"}
