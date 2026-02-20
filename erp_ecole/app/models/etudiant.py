"""
Modèle de données - Etudiant
============================
Représente un étudiant de l'école.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Etudiant(Base):
    """Modèle Etudiant"""
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, index=True)
    prenom = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telephone = Column(String(20), nullable=True)
    date_naissance = Column(DateTime, nullable=True)
    adresse = Column(String(500), nullable=True)
    matricule = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    inscriptions = relationship("Inscription", back_populates="etudiant")
    notes = relationship("Note", back_populates="etudiant")
