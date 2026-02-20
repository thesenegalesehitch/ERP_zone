"""
Modèle de données - Transaction
================================
Représente une transaction bancaire (débit, crédit, virement).
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class TypeTransaction(str, enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"
    VIREMENT = "virement"


class Transaction(Base):
    """Modèle Transaction"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    compte_id = Column(Integer, ForeignKey("comptes.id"), nullable=False)
    type_transaction = Column(SQLEnum(TypeTransaction), nullable=False)
    montant = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)
    date_transaction = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    compte = relationship("Compte", back_populates="transactions")
