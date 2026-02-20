"""
Modèle de données - Commande
============================
Représente une commande au restaurant.
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class StatutCommande(str, enum.Enum):
    EN_ATTENTE = "en_attente"
    EN_PREPARATION = "en_preparation"
    SERVIE = "servie"
    PAYEE = "payee"
    ANNULEE = "annulee"


class Commande(Base):
    """Modèle Commande"""
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    statut = Column(SQLEnum(StatutCommande), default=StatutCommande.EN_ATTENTE, nullable=False)
    montant_total = Column(Float, default=0.0, nullable=False)
    date_commande = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    table = relationship("Table")
