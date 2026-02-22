"""
Demandes de congé pour les employés

Ce module définit le modèle des demandes de congé
pour le système de gestion des ressources humaines.

Ce fichier fait partie du projet ERP développé pour le Sénégal.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.core.database import Base


class LeaveType(str, enum.Enum):
    """Types de congé"""
    CONGÉ_ANNUEL = "conge_annuel"
    CONGÉ_MALADIE = "conge_maladie"
    CONGÉ_MATERNITÉ = "conge_maternite"
    CONGÉ_PATERNITÉ = "conge_paternite"
    CONGÉ_SANS_SOLDE = "conge_sans_solde"
    PERMISSION = "permission"


class LeaveStatus(str, enum.Enum):
    """Statut de la demande de congé"""
    EN_ATTENTE = "en_attente"
    APPROUVÉE = "approuvee"
    REJETÉE = "rejetee"
    ANNULÉE = "annulee"


class LeaveRequest(Base):
    """Modèle des demandes decongé"""
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Employé
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Type de congé
    leave_type = Column(SQLEnum(LeaveType), nullable=False)
    
    # Dates
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    total_days = Column(Integer, nullable=False)
    
    # Statut
    status = Column(SQLEnum(LeaveStatus), default=LeaveStatus.EN_ATTENTE)
    
    # Motif
    reason = Column(Text, nullable=True)
    
    # Approbateur
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_date = Column(DateTime, nullable=True)
    approval_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relations
    employee = relationship("Employee", backref="leave_requests")
    
    def __repr__(self):
        return f"<LeaveRequest {self.employee_id} - {self.leave_type}>"
