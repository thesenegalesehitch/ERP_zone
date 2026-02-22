"""
Schémas de validation pour les demandes decongé

Ce module définit les schémas Pydantic pour la validation
des données des demandes decongé.

Ce fichier fait partie du projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LeaveRequestBase(BaseModel):
    """Base schema pour les demandes decongé"""
    leave_type: str
    start_date: datetime
    end_date: datetime


class LeaveRequestCreate(LeaveRequestBase):
    """Schema pour créer une demande decongé"""
    employee_id: int
    reason: Optional[str] = None


class LeaveRequestUpdate(BaseModel):
    """Schema pour mettre à jour une demande decongé"""
    status: Optional[str] = None
    approved_by: Optional[int] = None
    approved_date: Optional[datetime] = None
    approval_notes: Optional[str] = None


class LeaveRequestResponse(LeaveRequestBase):
    """Schema pour la réponse d'une demande decongé"""
    id: int
    employee_id: int
    total_days: int
    status: str
    reason: Optional[str]
    approved_by: Optional[int]
    approved_date: Optional[datetime]
    approval_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
