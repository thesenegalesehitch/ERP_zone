from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "ERP Zone RH Module"
    PROJECT_VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for Human Resources module of ERP Zone"

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/erp_zone_rh"

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()