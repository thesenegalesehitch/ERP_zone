"""
Schémas de validation pour les clients

Ce module définit les schémas Pydantic pour la validation
des données liées aux clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ClientBase(BaseModel):
    """Schéma de base pour un client"""
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    address: Optional[str] = None


class ClientCreate(ClientBase):
    """Schéma pour créer un client"""
    client_type: str = Field(default="particulier")
    company: Optional[str] = None
    contact_person: Optional[str] = None


class ClientUpdate(BaseModel):
    """Schéma pour mettre à jour un client"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    address: Optional[str] = None
    client_type: Optional[str] = None
    company: Optional[str] = None
    contact_person: Optional[str] = None
    status: Optional[str] = None


class ClientResponse(ClientBase):
    """Schéma pour la réponse d'un client"""
    id: int
    client_type: str
    company: Optional[str] = None
    contact_person: Optional[str] = None
    status: str
    total_revenue: float = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LeadCreate(BaseModel):
    """Schéma pour créer un prospect"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    company: Optional[str] = None
    source: str
    estimated_value: Optional[float] = None


class LeadUpdate(BaseModel):
    """Schéma pour mettre à jour un prospect"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    estimated_value: Optional[float] = None
    score: Optional[float] = None


class LeadResponse(BaseModel):
    """Schéma pour la réponse d'un prospect"""
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    source: str
    status: str
    estimated_value: Optional[float] = None
    score: Optional[float] = None
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InteractionCreate(BaseModel):
    """Schéma pour créer une interaction"""
    client_id: Optional[int] = None
    lead_id: Optional[int] = None
    interaction_type: str
    subject: str
    notes: Optional[str] = None


class InteractionResponse(BaseModel):
    """Schéma pour la réponse d'une interaction"""
    id: int
    client_id: Optional[int] = None
    lead_id: Optional[int] = None
    interaction_type: str
    subject: str
    notes: Optional[str] = None
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ClientFilter(BaseModel):
    """Schéma pour filtrer les clients"""
    client_type: Optional[str] = None
    status: Optional[str] = None
    search: Optional[str] = None


class LeadFilter(BaseModel):
    """Schéma pour filtrer les prospects"""
    source: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
