"""
Schémas de validation pour la gestion bancaire

Ce module définit les schémas Pydantic pour la validation
des données bancaires et transactions.

Ce fichier fait partie du projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BankAccountBase(BaseModel):
    """Base schema pour les comptes bancaires"""
    account_number: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    bank_name: str = Field(..., min_length=1, max_length=200)


class BankAccountCreate(BankAccountBase):
    """Schema pour créer un compte bancaire"""
    account_type: str = "courant"
    bank_code: Optional[str] = None
    agency: Optional[str] = None
    holder_name: str
    holder_id: Optional[str] = None
    initial_balance: float = 0
    opening_date: datetime


class BankAccountUpdate(BaseModel):
    """Schema pour mettre à jour un compte bancaire"""
    name: Optional[str] = None
    account_type: Optional[str] = None
    bank_name: Optional[str] = None
    bank_code: Optional[str] = None
    agency: Optional[str] = None
    holder_name: Optional[str] = None
    current_balance: Optional[float] = None
    closing_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    notes: Optional[str] = None


class BankAccountResponse(BankAccountBase):
    """Schema pour la réponse d'un compte bancaire"""
    id: int
    account_type: str
    bank_code: Optional[str]
    agency: Optional[str]
    holder_name: str
    holder_id: Optional[str]
    initial_balance: float
    current_balance: float
    opening_date: datetime
    closing_date: Optional[datetime]
    is_active: bool
    is_default: bool
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BankTransactionBase(BaseModel):
    """Base schema pour les transactions"""
    account_id: int
    transaction_type: str
    amount: float


class BankTransactionCreate(BankTransactionBase):
    """Schema pour créer une transaction"""
    date: datetime
    description: Optional[str] = None
    reference: Optional[str] = None
    counterparty_name: Optional[str] = None
    counterparty_account: Optional[str] = None
    counterparty_bank: Optional[str] = None
    category: Optional[str] = None


class BankTransactionUpdate(BaseModel):
    """Schema pour mettre à jour une transaction"""
    description: Optional[str] = None
    reference: Optional[str] = None
    counterparty_name: Optional[str] = None
    counterparty_account: Optional[str] = None
    counterparty_bank: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None


class BankTransactionResponse(BankTransactionBase):
    """Schema pour la réponse d'une transaction"""
    id: int
    transaction_number: str
    date: datetime
    description: Optional[str]
    reference: Optional[str]
    balance_before: float
    balance_after: float
    counterparty_name: Optional[str]
    counterparty_account: Optional[str]
    counterparty_bank: Optional[str]
    status: str
    category: Optional[str]
    recorded_by: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class CheckBase(BaseModel):
    """Base schema pour les chèques"""
    check_number: str = Field(..., min_length=1, max_length=50)
    check_date: datetime
    amount: float
    drawer_name: str = Field(..., min_length=1, max_length=200)


class CheckCreate(CheckBase):
    """Schema pour créer un chèque"""
    due_date: Optional[datetime] = None
    drawer_bank: Optional[str] = None
    drawer_account: Optional[str] = None
    beneficiary_name: Optional[str] = None
    bank_account_id: Optional[int] = None


class CheckUpdate(BaseModel):
    """Schema pour mettre à jour un chèque"""
    due_date: Optional[datetime] = None
    beneficiary_name: Optional[str] = None
    status: Optional[str] = None
    collection_date: Optional[datetime] = None
    bank_account_id: Optional[int] = None


class CheckResponse(CheckBase):
    """Schema pour la réponse d'un chèque"""
    id: int
    due_date: Optional[datetime]
    drawer_bank: Optional[str]
    drawer_account: Optional[str]
    beneficiary_name: Optional[str]
    status: str
    bank_account_id: Optional[int]
    collection_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BankReconciliation(BaseModel):
    """Rapprochement bancaire"""
    account_id: int
    date: datetime
    bank_balance: float
    book_balance: float
    transactions: List[dict]
