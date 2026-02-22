"""
Schémas de validation pour les ventes

Ce module définit les schémas Pydantic pour la validation
des données liées aux ventes.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SaleItem(BaseModel):
    """Article de vente"""
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    discount: float = Field(default=0, ge=0)


class SaleCreate(BaseModel):
    """Schéma pour créer une vente"""
    items: List[SaleItem]
    client_id: Optional[int] = None
    payment_method: str = Field(default="especes")
    sale_type: str = Field(default="comptoir")
    table_id: Optional[int] = None


class SaleUpdate(BaseModel):
    """Schéma pour mettre à jour une vente"""
    status: Optional[str] = None
    paid_amount: Optional[float] = None


class SaleResponse(BaseModel):
    """Schéma pour la réponse d'une vente"""
    id: int
    items: List[dict]
    subtotal: float
    tax_amount: float
    discount: float
    total: float
    paid_amount: float = 0
    change_amount: float = 0
    status: str
    payment_method: str
    sale_type: str
    table_id: Optional[int] = None
    client_id: Optional[int] = None
    cashier_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    """Schéma pour créer un paiement"""
    sale_id: int
    amount: float = Field(..., gt=0)
    payment_method: str


class PaymentResponse(BaseModel):
    """Schéma pour la réponse d'un paiement"""
    id: int
    sale_id: int
    amount: float
    payment_method: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TableBase(BaseModel):
    """Schéma de base pour une table"""
    table_number: str = Field(..., min_length=1, max_length=10)
    capacity: int = Field(default=4, ge=1)


class TableCreate(TableBase):
    """Schéma pour créer une table"""
    section: Optional[str] = None


class TableUpdate(BaseModel):
    """Schéma pour mettre à jour une table"""
    table_number: Optional[str] = Field(None, min_length=1, max_length=10)
    capacity: Optional[int] = Field(None, ge=1)
    status: Optional[str] = None


class TableResponse(TableBase):
    """Schéma pour la réponse d'une table"""
    id: int
    section: Optional[str] = None
    status: str
    current_order_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CartItem(BaseModel):
    """Article du panier"""
    product_id: int
    quantity: int = Field(..., gt=0)


class CartResponse(BaseModel):
    """Schéma pour la réponse du panier"""
    items: List[dict]
    subtotal: float
    tax_amount: float
    total: float
    item_count: int
    
    class Config:
        from_attributes = True


class SaleFilter(BaseModel):
    """Schéma pour filtrer les ventes"""
    status: Optional[str] = None
    payment_method: Optional[str] = None
    sale_type: Optional[str] = None
    cashier_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class DailySalesReport(BaseModel):
    """Schéma pour le rapport des ventes quotidiennes"""
    date: datetime
    total_sales: int
    total_revenue: float
    average_sale: float
    items_sold: int
    
    class Config:
        from_attributes = True
