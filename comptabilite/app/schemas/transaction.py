"""
Schémas de validation pour les transactions

Ce module définit les schémas Pydantic pour la validation
des données liées aux transactions comptables.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AccountBase(BaseModel):
    """Schéma de base pour un compte"""
    code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=200)
    account_type: str


class AccountCreate(AccountBase):
    """Schéma pour créer un compte"""
    parent_id: Optional[int] = None
    description: Optional[str] = None


class AccountUpdate(BaseModel):
    """Schéma pour mettre à jour un compte"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class AccountResponse(AccountBase):
    """Schéma pour la réponse d'un compte"""
    id: int
    parent_id: Optional[int] = None
    description: Optional[str] = None
    balance: float = 0
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TransactionLine(BaseModel):
    """Ligne de transaction"""
    account_id: int
    debit: float = Field(default=0, ge=0)
    credit: float = Field(default=0, ge=0)
    description: Optional[str] = None


class TransactionCreate(BaseModel):
    """Schéma pour créer une transaction"""
    journal_type: str
    date: datetime
    description: str
    lines: List[TransactionLine]
    reference: Optional[str] = None


class TransactionResponse(BaseModel):
    """Schéma pour la réponse d'une transaction"""
    id: int
    journal_type: str
    date: datetime
    description: str
    reference: Optional[str] = None
    total_debit: float
    total_credit: float
    status: str
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    """Schéma de base pour une facture"""
    client_id: int
    invoice_number: str


class InvoiceCreate(InvoiceBase):
    """Schéma pour créer une facture"""
    items: List[dict]
    payment_terms: Optional[str] = None
    due_date: Optional[datetime] = None


class InvoiceUpdate(BaseModel):
    """Schéma pour mettre à jour une facture"""
    status: Optional[str] = None
    paid_amount: Optional[float] = None


class InvoiceResponse(InvoiceBase):
    """Schéma pour la réponse d'une facture"""
    id: int
    items: List[dict]
    subtotal: float
    tax_amount: float
    total: float
    paid_amount: float = 0
    status: str
    payment_terms: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    """Schéma pour créer un paiement"""
    invoice_id: int
    amount: float = Field(..., gt=0)
    payment_method: str
    reference: Optional[str] = None


class PaymentResponse(BaseModel):
    """Schéma pour la réponse d'un paiement"""
    id: int
    invoice_id: int
    amount: float
    payment_method: str
    reference: Optional[str] = None
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionFilter(BaseModel):
    """Schéma pour filtrer les transactions"""
    journal_type: Optional[str] = None
    account_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AccountFilter(BaseModel):
    """Schéma pour filtrer les comptes"""
    account_type: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
