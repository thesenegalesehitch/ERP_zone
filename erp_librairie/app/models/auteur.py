"""
Modèle de données - Auteur
==========================
Représente les auteurs de livres.

Attributs:
- id: Identifiant unique
- nom: Nom de l'auteur
- prenom: Prénom de l'auteur
- bibliographie: Biographie de l'auteur
- created_at: Date de création
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Auteur(Base):
    """Modèle Auteur - Auteurs de livres"""
    
    __tablename__ = "auteurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, index=True)
    prenom = Column(String(100), nullable=True)
    bibliographie = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relation plusieurs-à-plusieurs avec les livres
    livres = relationship("Livre", secondary="livre_auteurs", back_populates="auteurs")
