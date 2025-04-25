"""
Configuration settings for the Julep Research Assistant application.

This module contains configuration settings that are loaded from environment variables.
"""

import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # API settings
    API_TITLE: str = "Julep Research Assistant API"
    API_DESCRIPTION: str = "API for research assistant powered by Julep AI"
    API_VERSION: str = "0.1.0"
    
    # Julep settings
    JULEP_API_KEY: str
    JULEP_MODEL: str = "gpt-4o"
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """
    Get application settings.
    
    Returns:
        Settings: Application settings loaded from environment variables.
    """
    return Settings()