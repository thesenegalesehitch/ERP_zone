"""
Configuration de l'application ERP Banque
=========================================
Paramètres de configuration pour le module bancaire.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Paramètres de configuration de l'application"""
    PROJECT_NAME: str = "ERP Zone - Module Banque"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/erp_zone_banque"
    SECRET_KEY: str = "banque-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
