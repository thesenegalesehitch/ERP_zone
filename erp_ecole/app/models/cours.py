"""
Modèle de données - Cours
=========================
Représente un cours dans l'école.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Cours(Base):
    """Modèle Cours"""
    __tablename__ = "cours"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(200), nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(String(1000), nullable=True)
    credits = Column(Integer, default=0, nullable=False)
    professeur_id = Column(Integer, ForeignKey("professeurs.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    inscriptions = relationship("Inscription", back_populates="cours")
    notes = relationship("Note", back_populates="cours")
