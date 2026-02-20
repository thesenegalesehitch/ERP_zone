"""
Modèle de données - Client Bancaire
====================================
Représente un client de la banque.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class ClientBancaire(Base):
    """Modèle Client Bancaire"""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, index=True)
    prenom = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telephone = Column(String(20), nullable=True)
    adresse = Column(String(500), nullable=True)
    numero_piece = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    comptes = relationship("Compte", back_populates="client")
