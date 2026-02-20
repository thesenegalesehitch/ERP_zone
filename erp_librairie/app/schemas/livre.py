"""
Schémas de validation - Livre
==============================
Schémas Pydantic pour la validation des données Livre.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class LivreBase(BaseModel):
    """Schéma de base pour un livre"""
    titre: str = Field(..., description="Titre du livre")
    isbn: str = Field(..., description="Numéro ISBN (13 caractères)")
    prix: float = Field(..., ge=0, description="Prix de vente en euros")
    stock_quantite: int = Field(default=0, ge=0, description="Quantité en stock")
    categorie_id: Optional[int] = Field(None, description="ID de la catégorie")
    description: Optional[str] = Field(None, description="Résumé du livre")
    est_actif: bool = Field(default=True, description="Disponibilité à la vente")


class LivreCreate(LivreBase):
    """Schéma pour créer un nouveau livre"""
    pass


class LivreUpdate(BaseModel):
    """Schéma pour mettre à jour un livre"""
    titre: Optional[str] = None
    isbn: Optional[str] = None
    prix: Optional[float] = None
    stock_quantite: Optional[int] = None
    categorie_id: Optional[int] = None
    description: Optional[str] = None
    est_actif: Optional[bool] = None


class LivreResponse(LivreBase):
    """Schéma de réponse pour un livre"""
    id: int
    date_publication: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
