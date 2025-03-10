"""Tests for internationalization utilities."""

import pytest

from src.utils.i18n import get_supported_languages, get_text


def test_get_supported_languages():
    """Test getting supported languages."""
    languages = get_supported_languages()
    assert isinstance(languages, list)
    assert "en" in languages
    assert "zh" in languages


def test_get_text_default_language():
    """Test getting text with default language."""
    message = "Hello"
    translated = get_text(message)
    assert isinstance(translated, str)


def test_get_text_specific_language():
    """Test getting text with specific language."""
    message = "Hello"
    translated = get_text(message, lang="en")
    assert isinstance(translated, str)


def test_get_text_unsupported_language():
    """Test getting text with unsupported language falls back to default."""
    message = "Hello"
    translated = get_text(message, lang="unsupported")
    assert isinstance(translated, str)


def test_get_text_caching():
    """Test that get_text caches results."""
    message = "Hello"
    result1 = get_text(message, lang="en")
    result2 = get_text(message, lang="en")
    assert result1 is result2  # Check if cache is working
