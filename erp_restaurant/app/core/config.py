"""
Configuration - ERP Restaurant
==============================
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ERP Zone - Module Restaurant"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/erp_zone_restaurant"
    SECRET_KEY: str = "restaurant-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
