"""Global settings configuration."""

from pathlib import Path
from typing import Dict, Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Global settings for the project."""

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    SRC_ROOT: Path = PROJECT_ROOT / "src"
    RESOURCES_ROOT: Path = PROJECT_ROOT / "resources"

    # Environment
    ENV: str = Field(default="development", env="APP_ENV")
    DEBUG: bool = Field(default=True, env="APP_DEBUG")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")

    # Internationalization
    DEFAULT_LANGUAGE: str = Field(default="en", env="DEFAULT_LANGUAGE")
    SUPPORTED_LANGUAGES: list[str] = Field(default=["en", "zh"], env="SUPPORTED_LANGUAGES")

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "Project API"
    API_DESCRIPTION: str = "API documentation for the project"
    API_VERSION: str = "1.0.0"

    class Config:
        """Pydantic config class."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
