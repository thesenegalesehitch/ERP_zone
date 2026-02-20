"""
Configuration de l'application ERP Librairie
============================================
Paramètres globaux de l'application incluant
- Nom du projet
- Version de l'API
- Configuration de la base de données
- Paramètres de sécurité JWT
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Paramètres de configuration de l'application"""
    
    # Nom du projet affiché dans la documentation API
    PROJECT_NAME: str = "ERP Zone - Module Librairie"
    
    # Version de l'API (sémantique)
    PROJECT_VERSION: str = "1.0.0"
    
    # Chaîne de connexion PostgreSQL
    # Format: postgresql://utilisateur:motdepasse@host:port/nom_bdd
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/erp_zone_librairie"
    
    # Clé secrète pour la signature des tokens JWT
    # IMPORTANT: Changer en production!
    SECRET_KEY: str = "librairie-secret-key-change-in-production"
    
    # Algorithme de chiffrement JWT
    ALGORITHM: str = "HS256"
    
    # Durée de validité du token en minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Fichier .env pour les variables d'environnement
        env_file = ".env"
        # Respecter la casse des variables
        case_sensitive = True


# Instance singleton des paramètres
settings = Settings()
