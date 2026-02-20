from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ERP Zone Accounting Module"
    PROJECT_VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for Accounting module of ERP Zone"
    
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/erp_zone_accounting"
    
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
