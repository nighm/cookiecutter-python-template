"""Tests for logging utilities."""

import structlog

from src.utils.logging import configure_logging, get_logger


def test_configure_logging():
    """Test logging configuration."""
    configure_logging()
    # Configuration should not raise any exceptions


def test_get_logger():
    """Test getting logger instance."""
    logger = get_logger("test")
    assert isinstance(logger, structlog.BoundLogger)


def test_get_logger_with_name():
    """Test getting logger with specific name."""
    logger = get_logger("custom_name")
    assert isinstance(logger, structlog.BoundLogger)


def test_get_logger_without_name():
    """Test getting logger without name."""
    logger = get_logger()
    assert isinstance(logger, structlog.BoundLogger)
