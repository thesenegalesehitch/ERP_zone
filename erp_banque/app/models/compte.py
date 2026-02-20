"""
Modèle de données - Compte Bancaire
====================================
Représente un compte bancaire (courant, épargne, etc.)
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class TypeCompte(str, enum.Enum):
    COURANT = "courant"
    EPARGNE = "epargne"
    JOINT = "joint"


class Compte(Base):
    """Modèle Compte Bancaire"""
    __tablename__ = "comptes"

    id = Column(Integer, primary_key=True, index=True)
    numero_compte = Column(String(20), unique=True, nullable=False, index=True)
    type_compte = Column(SQLEnum(TypeCompte), default=TypeCompte.COURANT, nullable=False)
    solde = Column(Float, nullable=False, default=0.0)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    est_actif = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    client = relationship("ClientBancaire", back_populates="comptes")
    transactions = relationship("Transaction", back_populates="compte")
