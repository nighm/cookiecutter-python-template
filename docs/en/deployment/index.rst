Deployment Guide
===============

Docker Deployment
--------------

Prerequisites
^^^^^^^^^^^

* Docker
* Docker Compose

Configuration
^^^^^^^^^^^

The project includes three Docker services:

1. Application Service (app)
   * Runs the main application
   * Exposes port 8000
   * Mounts source code for development

2. Documentation Service (docs)
   * Serves live documentation
   * Exposes port 8080
   * Auto-rebuilds on changes

3. Test Service (test)
   * Runs test suite
   * Generates coverage reports

Environment Variables
^^^^^^^^^^^^^^^^^^

Configure the following environment variables:

.. code-block:: ini

    APP_ENV=development
    APP_DEBUG=true
    LOG_LEVEL=INFO
    LOG_FORMAT=console
    DEFAULT_LANGUAGE=en

Deployment Steps
^^^^^^^^^^^^^

1. Build and start services::

    docker-compose up --build

2. Run tests::

    docker-compose run test

3. View documentation::

    docker-compose up docs

Production Deployment
------------------

Prerequisites
^^^^^^^^^^^

* Python 3.8+
* Poetry
* PostgreSQL (optional)
* Redis (optional)

Steps
^^^^^

1. Install dependencies::

    poetry install --no-dev

2. Set environment variables::

    export APP_ENV=production
    export APP_DEBUG=false
    export LOG_LEVEL=WARNING
    export LOG_FORMAT=json

3. Run migrations (if applicable)::

    poetry run python -m src.db.migrations

4. Start application::

    poetry run python -m src

Monitoring
---------

Health Checks
^^^^^^^^^^^

The application exposes health check endpoints:

* ``/health``: Basic health check
* ``/health/live``: Liveness probe
* ``/health/ready``: Readiness probe

Metrics
^^^^^^

Prometheus metrics are available at ``/metrics``.

Logging
^^^^^^

Logs are written to stdout in JSON format in production.

Security
-------

Best Practices
^^^^^^^^^^^^

1. Use non-root user in Docker
2. Keep dependencies updated
3. Enable security middleware
4. Use HTTPS in production
5. Implement rate limiting

Environment Variables
^^^^^^^^^^^^^^^^^^

Never commit sensitive information:

* Use environment variables
* Use secrets management
* Rotate credentials regularly

Backup
-----

Database
^^^^^^^

1. Regular automated backups
2. Test restore procedures
3. Encrypt backup data

Configuration
^^^^^^^^^^^

1. Version control configs
2. Separate sensitive data
3. Document all settings

Disaster Recovery
^^^^^^^^^^^^^^

1. Document recovery procedures
2. Regular recovery testing
3. Maintain backup infrastructure
