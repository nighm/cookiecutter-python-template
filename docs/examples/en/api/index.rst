API Documentation
================

Core Module
---------

Compatibility
^^^^^^^^^^^

.. automodule:: src.core.compatibility
   :members:
   :undoc-members:
   :show-inheritance:

Utility Module
------------

Logging
^^^^^^^

.. automodule:: src.utils.logging
   :members:
   :undoc-members:
   :show-inheritance:

Internationalization
^^^^^^^^^^^^^^^^^

.. automodule:: src.utils.i18n
   :members:
   :undoc-members:
   :show-inheritance:

Decorators
^^^^^^^^^

.. automodule:: src.utils.decorators
   :members:
   :undoc-members:
   :show-inheritance:

Configuration Module
-----------------

Global Settings
^^^^^^^^^^^^^

.. automodule:: src.config.settings
   :members:
   :undoc-members:
   :show-inheritance:

Monitoring
---------

Health Checks
^^^^^^^^^^^

The application provides health check endpoints to monitor its status:

.. code-block:: python

    from src.monitoring import health

    @app.get("/health")
    async def health_check():
        """Basic health check."""
        return health.check_health()

    @app.get("/health/live")
    async def liveness():
        """Kubernetes liveness probe."""
        return health.check_liveness()

    @app.get("/health/ready")
    async def readiness():
        """Kubernetes readiness probe."""
        return health.check_readiness()

Metrics
^^^^^^

Prometheus metrics are exposed via the `/metrics` endpoint:

.. code-block:: python

    from src.monitoring import metrics

    # Counter metric example
    request_count = metrics.counter(
        "http_requests_total",
        "Total HTTP requests count",
        ["method", "endpoint", "status"]
    )

    # Histogram metric example
    request_latency = metrics.histogram(
        "http_request_duration_seconds",
        "HTTP request duration in seconds",
        ["method", "endpoint"]
    )

Logging
^^^^^^

Structured logging configuration:

.. code-block:: python

    from src.utils.logging import configure_logging

    # Configure logging with default settings
    configure_logging()

    # Configure logging with custom settings
    configure_logging(
        log_level="DEBUG",
        log_format="json",
        log_file="app.log"
    )

Example Usage
^^^^^^^^^^^

.. code-block:: python

    from src.utils.logging import get_logger

    logger = get_logger(__name__)

    # Log messages with different levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

    # Log with context
    logger.info("User action", extra={
        "user_id": "123",
        "action": "login",
        "status": "success"
    })
