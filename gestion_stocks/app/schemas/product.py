"""
Schémas de validation pour les produits

Ce module définit les schémas Pydantic pour la validation
des données liées aux produits.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """Schéma de base pour un produit"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    sku: str = Field(..., min_length=1, max_length=50)
    barcode: Optional[str] = None
    category: Optional[str] = None


class ProductCreate(ProductBase):
    """Schéma pour créer un produit"""
    unit_price: float = Field(..., gt=0)
    cost_price: float = Field(..., ge=0)
    quantity: int = Field(default=0, ge=0)
    reorder_point: int = Field(default=10, ge=0)
    warehouse_id: Optional[int] = None


class ProductUpdate(BaseModel):
    """Schéma pour mettre à jour un produit"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    barcode: Optional[str] = None
    category: Optional[str] = None
    unit_price: Optional[float] = Field(None, gt=0)
    cost_price: Optional[float] = Field(None, ge=0)
    reorder_point: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """Schéma pour la réponse d'un produit"""
    id: int
    unit_price: float
    cost_price: float
    quantity: int
    reorder_point: int
    warehouse_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockMovementCreate(BaseModel):
    """Schéma pour créer un mouvement de stock"""
    product_id: int
    movement_type: str = Field(...)
    quantity: int = Field(..., gt=0)
    reason: Optional[str] = None
    reference: Optional[str] = None


class StockMovementResponse(BaseModel):
    """Schéma pour la réponse d'un mouvement de stock"""
    id: int
    product_id: int
    movement_type: str
    quantity: int
    previous_quantity: int
    new_quantity: int
    reason: Optional[str] = None
    reference: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class StockAdjustmentCreate(BaseModel):
    """Schéma pour créer un ajustement de stock"""
    product_id: int
    new_quantity: int = Field(..., ge=0)
    reason: str


class StockAdjustmentResponse(BaseModel):
    """Schéma pour la réponse d'un ajustement de stock"""
    id: int
    product_id: int
    old_quantity: int
    new_quantity: int
    difference: int
    reason: str
    adjusted_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductFilter(BaseModel):
    """Schéma pour filtrer les produits"""
    category: Optional[str] = None
    warehouse_id: Optional[int] = None
    low_stock: Optional[bool] = None
    search: Optional[str] = None


class StockReport(BaseModel):
    """Schéma pour le rapport de stock"""
    product_id: int
    product_name: str
    current_stock: int
    reorder_point: int
    status: str
    
    class Config:
        from_attributes = True
