"""
Module des modèles de demandes de congés

Ce module définit les modèles de données pour la gestion des congés.
"""
from sqlalchemy import Column, Integer, Date, String, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum as PyEnum


class LeaveType(PyEnum):
    """Types de congés"""
    ANNUAL = "annual"           # Congé annuel
    SICK = "sick"              # Maladie
    MATERNITY = "maternity"    # Maternité
    PATERNITY = "paternity"    # Paternité
    UNPAID = "unpaid"          # Sans solde
    WORK_ACCIDENT = "work_accident"  # Accident du travail
    OTHER = "other"            # Autre


class LeaveStatus(PyEnum):
    """Statuts des demandes de congés"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class LeaveRequest(Base):
    """
    Modèle LeaveRequest - Demande decongé
    
    Attributs:
        id: Identifiant unique
        employee_id: ID de l'employé
        leave_type: Type de congé
        start_date: Date de début
        end_date: Date de fin
        days_count: Nombre de jours
        reason: Raison/Motif
        status: Statut de la demande
        approved_by: ID de l'approbateur
        approved_date: Date d'approbation
        rejection_reason: Raison du rejet
    """
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    leave_type = Column(Enum(LeaveType), default=LeaveType.ANNUAL, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days_count = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING, nullable=False)
    
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_date = Column(Date, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    employee = relationship("Employee", back_populates="leave_requests")


class LeaveBalance(Base):
    """
    Modèle LeaveBalance - Solde de congés
    
    Suit le nombre de jours de congés restants pour chaque employé
    """
    __tablename__ = "leave_balances"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    leave_type = Column(Enum(LeaveType), default=LeaveType.ANNUAL, nullable=False)
    year = Column(Integer, nullable=False)
    total_days = Column(Float, nullable=False)  # Joursalloués
    used_days = Column(Float, default=0)  # Jours utilisés
    remaining_days = Column(Float, nullable=False)  # Jours restants


class Holiday(Base):
    """
    Modèle Holiday - Jours fériés
    
    Définit les jours fériés dans le calendrier
    """
    __tablename__ = "holidays"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    date = Column(Date, nullable=False, unique=True)
    is_active = Column(String(10), default="yes")  # yes, no
    description = Column(Text)