"""
Configuration - ERP Ecole
=========================
Configuration pour le module école.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ERP Zone - Module Ecole"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/erp_zone_ecole"
    SECRET_KEY: str = "ecole-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
