"""
Configuration settings for the FastAPI Todo application.
Load environment variables and define settings.
"""

import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Basic info
    APP_NAME: str = "Todo API"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todos.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"


settings = Settings()