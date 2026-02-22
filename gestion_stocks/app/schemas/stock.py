"""
Schémas de validation pour les stocks

Ce module définit les schémas Pydantic pour la validation
des données des produits et mouvements de stock.

Ce fichier fait partie du projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductCategoryBase(BaseModel):
    """Base schema pour les catégories"""
    code: str
    name: str


class ProductCategoryCreate(ProductCategoryBase):
    """Schema pour créer une catégorie"""
    description: Optional[str] = None
    parent_id: Optional[int] = None
    tax_rate: float = 18


class ProductCategoryUpdate(BaseModel):
    """Schema pour mettre à jour une catégorie"""
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    tax_rate: Optional[float] = None
    is_active: Optional[bool] = None


class ProductCategoryResponse(ProductCategoryBase):
    """Schema pour la réponse d'une catégorie"""
    id: int
    description: Optional[str]
    parent_id: Optional[int]
    tax_rate: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base schema pour les produits"""
    sku: str
    name: str


class ProductCreate(ProductBase):
    """Schema pour créer un produit"""
    description: Optional[str] = None
    barcode: Optional[str] = None
    category_id: Optional[int] = None
    unit: str = "pc"
    unit_price: float = 0
    cost_price: float = 0
    selling_price: float = 0
    minimum_stock: float = 0
    maximum_stock: float = 0
    warehouse_id: Optional[int] = None
    location: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None


class ProductUpdate(BaseModel):
    """Schema pour mettre à jour un produit"""
    name: Optional[str] = None
    description: Optional[str] = None
    barcode: Optional[str] = None
    category_id: Optional[int] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    current_stock: Optional[float] = None
    minimum_stock: Optional[float] = None
    maximum_stock: Optional[float] = None
    warehouse_id: Optional[int] = None
    location: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None
    notes: Optional[str] = None


class ProductResponse(ProductBase):
    """Schema pour la réponse d'un produit"""
    id: int
    description: Optional[str]
    barcode: Optional[str]
    category_id: Optional[int]
    unit: str
    unit_price: float
    cost_price: float
    selling_price: float
    current_stock: float
    minimum_stock: float
    maximum_stock: float
    warehouse_id: Optional[int]
    location: Optional[str]
    status: str
    is_active: bool
    image_url: Optional[str]
    weight: Optional[float]
    dimensions: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WarehouseBase(BaseModel):
    """Base schema pour les entrepôts"""
    code: str
    name: str


class WarehouseCreate(WarehouseBase):
    """Schema pour créer un entrepôt"""
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: str = "Sénégal"
    capacity: float = 0


class WarehouseUpdate(BaseModel):
    """Schema pour mettre à jour un entrepôt"""
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    capacity: Optional[float] = None
    is_active: Optional[bool] = None


class WarehouseResponse(WarehouseBase):
    """Schema pour la réponse d'un entrepôt"""
    id: int
    description: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: str
    capacity: float
    is_active: bool
    is_default: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockMovementBase(BaseModel):
    """Base schema pour les mouvements de stock"""
    product_id: int
    movement_type: str
    quantity: float


class StockMovementCreate(StockMovementBase):
    """Schema pour créer un mouvement de stock"""
    quantity_before: float
    quantity_after: float
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    from_warehouse_id: Optional[int] = None
    to_warehouse_id: Optional[int] = None
    reason: Optional[str] = None


class StockMovementResponse(StockMovementBase):
    """Schema pour la réponse d'un mouvement de stock"""
    id: int
    quantity_before: float
    quantity_after: float
    reference_type: Optional[str]
    reference_id: Optional[int]
    from_warehouse_id: Optional[int]
    to_warehouse_id: Optional[int]
    reason: Optional[str]
    recorded_by: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
