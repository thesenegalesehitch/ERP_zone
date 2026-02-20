"""
Configuration de la base de données - ERP Librairie
=====================================================
Module gérant la connexion à PostgreSQL et la création
des sessions de base de données pour les opérations ORM.

Fonctions:
- create_engine: Crée le moteur de connexion SQLAlchemy
- get_db: Générateur de session pour les dépendances FastAPI
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Création du moteur de base de données
# connect_args nécessaire pour PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# SessionLocal: classe pour créer des sessions de base de données
# autocommit=False: Commit manuel requis
# autoflush=False: Flush manuel requis
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Classe parente pour tous les modèles ORM
Base = declarative_base()


def get_db():
    """
    Générateur de session de base de données
    ========================================
    Fonction de dépendance FastAPI qui:
    1. Ouvre une session à chaque requête
    2. Yield la session au handler de route
    3. Ferme automatiquement la session après traitement
    
    Usage:
        @app.get("/livres")
        def liste_livres(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
