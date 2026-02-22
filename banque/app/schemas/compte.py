"""
Schémas de validation pour les comptes bancaires

Ce module définit les schémas Pydantic pour la validation
des données liées aux comptes bancaires.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BankAccountBase(BaseModel):
    """Schéma de base pour un compte bancaire"""
    account_number: str = Field(..., min_length=10, max_length=30)
    account_name: str = Field(..., min_length=1, max_length=200)


class BankAccountCreate(BankAccountBase):
    """Schéma pour créer un compte bancaire"""
    account_type: str = Field(default="compte_courant")
    balance: float = Field(default=0)
    currency: str = Field(default="XOF")
    overdraft_limit: float = Field(default=0)


class BankAccountUpdate(BaseModel):
    """Schéma pour mettre à jour un compte bancaire"""
    account_name: Optional[str] = Field(None, min_length=1, max_length=200)
    overdraft_limit: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None


class BankAccountResponse(BankAccountBase):
    """Schéma pour la réponse d'un compte bancaire"""
    id: int
    account_type: str
    balance: float
    currency: str
    overdraft_limit: float
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    """Schéma pour créer une transaction"""
    account_id: int
    transaction_type: str
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    reference: Optional[str] = None
    counterparty: Optional[str] = None


class TransactionResponse(BaseModel):
    """Schéma pour la réponse d'une transaction"""
    id: int
    account_id: int
    transaction_type: str
    amount: float
    balance_after: float
    description: Optional[str] = None
    reference: Optional[str] = None
    counterparty: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransferCreate(BaseModel):
    """Schéma pour créer un virement"""
    from_account_id: int
    to_account_id: int
    amount: float = Field(..., gt=0)
    description: Optional[str] = None


class TransferResponse(BaseModel):
    """Schéma pour la réponse d'un virement"""
    id: int
    from_account_id: int
    to_account_id: int
    amount: float
    description: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoanBase(BaseModel):
    """Schéma de base pour un prêt"""
    borrower_name: str
    amount: float = Field(..., gt=0)


class LoanCreate(LoanBase):
    """Schéma pour créer un prêt"""
    interest_rate: float = Field(default=10)
    term_months: int = Field(default=12)
    loan_type: str = Field(default="conso")


class LoanUpdate(BaseModel):
    """Schéma pour mettre à jour un prêt"""
    status: Optional[str] = None
    paid_amount: Optional[float] = None


class LoanResponse(LoanBase):
    """Schéma pour la réponse d'un prêt"""
    id: int
    interest_rate: float
    term_months: int
    loan_type: str
    monthly_payment: float
    total_interest: float
    total_amount: float
    paid_amount: float = 0
    status: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionFilter(BaseModel):
    """Schéma pour filtrer les transactions"""
    account_id: Optional[int] = None
    transaction_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
