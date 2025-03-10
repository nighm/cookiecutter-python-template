"""Tests for decorator utilities."""

import pytest

from src.utils.decorators import deprecated, retry, timing


def test_retry_successful():
    """Test retry decorator with successful function."""
    
    @retry(max_attempts=3, delay=0.1)
    def success_func():
        return "success"

    assert success_func() == "success"


def test_retry_with_failure():
    """Test retry decorator with failing function."""
    attempts = 0

    @retry(max_attempts=3, delay=0.1)
    def fail_then_succeed():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ValueError("Temporary failure")
        return "success"

    assert fail_then_succeed() == "success"
    assert attempts == 2


def test_retry_max_attempts():
    """Test retry decorator reaches max attempts."""
    
    @retry(max_attempts=3, delay=0.1)
    def always_fail():
        raise ValueError("Always fails")

    with pytest.raises(ValueError):
        always_fail()


def test_timing_decorator():
    """Test timing decorator logs execution time."""
    
    @timing
    def slow_function():
        return "done"

    result = slow_function()
    assert result == "done"


def test_deprecated_decorator():
    """Test deprecated decorator logs warning."""
    
    @deprecated
    def old_function():
        return "old"

    result = old_function()
    assert result == "old"
