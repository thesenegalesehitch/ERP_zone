"""
Schémas de validation pour les commandes

Ce module définit les schémas Pydantic pour la validation
des données liées aux commandes de restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OrderItem(BaseModel):
    """Article de commande"""
    menu_item_id: int
    quantity: int = Field(..., gt=0)
    notes: Optional[str] = None


class OrderCreate(BaseModel):
    """Schéma pour créer une commande"""
    table_id: Optional[int] = None
    items: List[OrderItem]
    order_type: str = Field(default="sur_place")
    customer_name: Optional[str] = None


class OrderUpdate(BaseModel):
    """Schéma pour mettre à jour une commande"""
    status: Optional[str] = None
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    """Schéma pour la réponse d'une commande"""
    id: int
    table_id: Optional[int] = None
    items: List[dict]
    subtotal: float
    tax_amount: float
    total: float
    status: str
    order_type: str
    customer_name: Optional[str] = None
    waiter_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MenuItemBase(BaseModel):
    """Schéma de base pour un article du menu"""
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    category: str


class MenuItemCreate(MenuItemBase):
    """Schéma pour créer un article du menu"""
    description: Optional[str] = None
    available: bool = Field(default=True)


class MenuItemUpdate(BaseModel):
    """Schéma pour mettre à jour un article du menu"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    available: Optional[bool] = None


class MenuItemResponse(MenuItemBase):
    """Schéma pour la réponse d'un article du menu"""
    id: int
    description: Optional[str] = None
    available: bool
    created_at: datetime
    updated_at: datetime
    
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


class ReservationCreate(BaseModel):
    """Schéma pour créer une réservation"""
    table_id: int
    customer_name: str
    customer_phone: str
    reservation_date: datetime
    guest_count: int = Field(..., ge=1)
    notes: Optional[str] = None


class ReservationResponse(BaseModel):
    """Schéma pour la réponse d'une réservation"""
    id: int
    table_id: int
    customer_name: str
    customer_phone: str
    reservation_date: datetime
    guest_count: int
    status: str
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderFilter(BaseModel):
    """Schéma pour filtrer les commandes"""
    status: Optional[str] = None
    order_type: Optional[str] = None
    table_id: Optional[int] = None
    waiter_id: Optional[int] = None
