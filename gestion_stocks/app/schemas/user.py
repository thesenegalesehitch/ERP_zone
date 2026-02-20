"""
Schémas de validation - Utilisateur
====================================
Schémas Pydantic pour la validation des données utilisateur.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Schéma de base pour un utilisateur"""
    email: EmailStr = Field(..., description="Email unique de l'utilisateur")
    username: str = Field(..., description="Nom d'utilisateur unique")
    full_name: Optional[str] = Field(None, description="Nom complet")


class UserCreate(UserBase):
    """Schéma pour créer un nouvel utilisateur"""
    password: str = Field(..., description="Mot de passe")


class UserUpdate(BaseModel):
    """Schéma pour mettre à jour un utilisateur"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


class UserResponse(UserBase):
    """Schéma de réponse pour un utilisateur"""
    id: int
    is_active: bool
    is_superuser: bool
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
