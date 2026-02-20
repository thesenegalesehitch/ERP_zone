"""
Modèle de données - Catégorie
=============================
Représente les catégories de livres (Roman, Science-Fiction, Thriller, etc.)

Attributs:
- id: Identifiant unique
- nom: Nom de la catégorie
- description: Description de la catégorie
- created_at: Date de création
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Categorie(Base):
    """Modèle Catégorie - Classification des livres"""
    
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relation avec les livres
    livres = relationship("Livre", back_populates="categorie")
