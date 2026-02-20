"""
Modèle de données - Table
========================
Représente une table du restaurant.
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from datetime import datetime
import enum

from app.core.database import Base


class StatutTable(str, enum.Enum):
    LIBRE = "libre"
    OCCUPEE = "occupee"
    RESERVEE = "reservée"
    NETTOYAGE = "nettoyage"


class Table(Base):
    """Modèle Table"""
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False, index=True)
    capacite = Column(Integer, nullable=False, default=4)
    statut = Column(SQLEnum(StatutTable), default=StatutTable.LIBRE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
