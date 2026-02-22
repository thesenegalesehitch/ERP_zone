"""
Schémas de validation pour les achats

Ce module définit les schémas Pydantic pour la validation
des données liées aux achats.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SupplierBase(BaseModel):
    """Schéma de base pour un fournisseur"""
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    address: Optional[str] = None


class SupplierCreate(SupplierBase):
    """Schéma pour créer un fournisseur"""
    supplier_type: str = Field(default="distributeur")
    contact_person: Optional[str] = None


class SupplierUpdate(BaseModel):
    """Schéma pour mettre à jour un fournisseur"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    address: Optional[str] = None
    supplier_type: Optional[str] = None
    contact_person: Optional[str] = None
    status: Optional[str] = None


class SupplierResponse(SupplierBase):
    """Schéma pour la réponse d'un fournisseur"""
    id: int
    supplier_type: str
    contact_person: Optional[str] = None
    status: str
    rating: float = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PurchaseOrderItem(BaseModel):
    """Article de commande"""
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class PurchaseOrderCreate(BaseModel):
    """Schéma pour créer un bon de commande"""
    supplier_id: int
    items: List[PurchaseOrderItem]
    priority: str = Field(default="normale")
    payment_terms: Optional[str] = None
    notes: Optional[str] = None


class PurchaseOrderUpdate(BaseModel):
    """Schéma pour mettre à jour un bon de commande"""
    status: Optional[str] = None
    notes: Optional[str] = None


class PurchaseOrderResponse(BaseModel):
    """Schéma pour la réponse d'un bon de commande"""
    id: int
    supplier_id: int
    items: List[dict]
    subtotal: float
    tax_amount: float
    total: float
    status: str
    priority: str
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PurchaseReceiptCreate(BaseModel):
    """Schéma pour créer une réception"""
    order_id: int
    items: List[dict]
    notes: Optional[str] = None


class PurchaseReceiptResponse(BaseModel):
    """Schéma pour la réponse d'une réception"""
    id: int
    order_id: int
    items: List[dict]
    notes: Optional[str] = None
    received_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PurchaseInvoiceCreate(BaseModel):
    """Schéma pour créer une facture d'achat"""
    order_id: int
    invoice_number: str
    amount: float = Field(..., gt=0)


class PurchaseInvoiceResponse(BaseModel):
    """Schéma pour la réponse d'une facture d'achat"""
    id: int
    order_id: int
    invoice_number: str
    amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class SupplierFilter(BaseModel):
    """Schéma pour filtrer les fournisseurs"""
    supplier_type: Optional[str] = None
    status: Optional[str] = None
    search: Optional[str] = None


class PurchaseOrderFilter(BaseModel):
    """Schéma pour filtrer les commandes"""
    status: Optional[str] = None
    supplier_id: Optional[int] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
