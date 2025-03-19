"""Version test module."""

from {{ cookiecutter.package_name }} import __version__


def test_version():
    """Test version is string."""
    assert isinstance(__version__, str) 