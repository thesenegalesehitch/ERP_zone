"""
Schémas de validation - Client
===============================
Schémas Pydantic pour la validation des données Client.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class ClientBase(BaseModel):
    """Schéma de base pour un client"""
    nom: str = Field(..., description="Nom du client")
    prenom: Optional[str] = Field(None, description="Prénom du client")
    email: EmailStr = Field(..., description="Email du client")
    telephone: Optional[str] = Field(None, description="Numéro de téléphone")
    adresse: Optional[str] = Field(None, description="Adresse postale")


class ClientCreate(ClientBase):
    """Schéma pour créer un nouveau client"""
    pass


class ClientUpdate(BaseModel):
    """Schéma pour mettre à jour un client"""
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None


class ClientResponse(ClientBase):
    """Schéma de réponse pour un client"""
    id: int
    points_fidelite: int
    created_at: datetime

    class Config:
        from_attributes = True
