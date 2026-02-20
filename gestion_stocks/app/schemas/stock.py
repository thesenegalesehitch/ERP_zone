"""
Schémas de validation - Mouvement de Stock
==========================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class StockMovementBase(BaseModel):
    """Schéma de base pour un mouvement de stock"""
    product_id: int = Field(..., description="ID du produit")
    quantity: int = Field(..., description="Quantité")
    movement_type: str = Field(..., description="Type: in/out")
    reference: Optional[str] = Field(None, description="Référence")


class StockMovementCreate(StockMovementBase):
    """Schéma pour créer un mouvement"""
    pass


class StockMovementResponse(StockMovementBase):
    """Schéma de réponse"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
