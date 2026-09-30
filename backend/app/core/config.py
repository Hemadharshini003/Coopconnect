import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CoopConnect AI"
    APP_ENV: str = "development"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-jwt-key-coopconnect-ai-2026-sih"
    JWT_SECRET_KEY: str = "super-secret-jwt-key-coopconnect-ai-2026-sih"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day for local demo convenience
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "sqlite:///./coopconnect.db"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000"
    ]

    LOG_LEVEL: str = "INFO"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
