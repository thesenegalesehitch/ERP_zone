"""
Modèle de données - Client
==========================
Représente les clients de la librairie.

Attributs:
- id: Identifiant unique
- nom: Nom du client
- prenom: Prénom du client
- email: Email unique
- telephone: Numéro de téléphone
- adresse: Adresse postale
- points_fidelite: Points de fidélité accumulés
- created_at: Date de création
"""

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Client(Base):
    """Modèle Client - Clients de la librairie"""
    
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, index=True)
    prenom = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telephone = Column(String(20), nullable=True)
    adresse = Column(String(500), nullable=True)
    points_fidelite = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relation avec les ventes
    ventes = relationship("Vente", back_populates="client")
