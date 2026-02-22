"""
Modèle de données pour les comptes financiers

Ce module définit le modèle de données pour les comptes
dans le module de comptabilité.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class AccountModel:
    """Modèle de compte"""
    
    def __init__(
        self,
        id: int,
        account_number: str,
        account_name: str,
        account_type: str = "actif",
        parent_id: Optional[int] = None,
        description: Optional[str] = None,
        balance: float = 0,
        currency: str = "XOF",
        is_active: bool = True,
        is_allow_transaction: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.account_number = account_number
        self.account_name = account_name
        self.account_type = account_type
        self.parent_id = parent_id
        self.description = description
        self.balance = balance
        self.currency = currency
        self.is_active = is_active
        self.is_allow_transaction = is_allow_transaction
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "account_number": self.account_number,
            "account_name": self.account_name,
            "account_type": self.account_type,
            "parent_id": self.parent_id,
            "description": self.description,
            "balance": self.balance,
            "currency": self.currency,
            "is_active": self.is_active,
            "is_allow_transaction": self.is_allow_transaction,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AccountModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            account_number=data.get("account_number"),
            account_name=data.get("account_name"),
            account_type=data.get("account_type", "actif"),
            parent_id=data.get("parent_id"),
            description=data.get("description"),
            balance=data.get("balance", 0),
            currency=data.get("currency", "XOF"),
            is_active=data.get("is_active", True),
            is_allow_transaction=data.get("is_allow_transaction", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.is_active
    
    def is_debit_balance(self) -> bool:
        """Vérifie si solde débiteur"""
        return self.account_type in ["actif", "charge"]
    
    def is_credit_balance(self) -> bool:
        """Vérifie si solde créditeur"""
        return self.account_type in ["passif", "produit", "capitaux_propres"]


class JournalEntryModel:
    """Modèle d'écriture comptable"""
    
    def __init__(
        self,
        id: int,
        entry_number: str,
        entry_date: datetime = None,
        description: str,
        reference: Optional[str] = None,
        total_debit: float = 0,
        total_credit: float = 0,
        status: str = "brouillon",
        posted_by: Optional[int] = None,
        posted_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.entry_number = entry_number
        self.entry_date = entry_date
        self.description = description
        self.reference = reference
        self.total_debit = total_debit
        self.total_credit = total_credit
        self.status = status
        self.posted_by = posted_by
        self.posted_at = posted_at
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "entry_number": self.entry_number,
            "entry_date": self.entry_date,
            "description": self.description,
            "reference": self.reference,
            "total_debit": self.total_debit,
            "total_credit": self.total_credit,
            "status": self.status,
            "posted_by": self.posted_by,
            "posted_at": self.posted_at,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_balanced(self) -> bool:
        """Vérifie si équilibrée"""
        return abs(self.total_debit - self.total_credit) < 0.01
    
    def is_posted(self) -> bool:
        """Vérifie si publiée"""
        return self.status == "publie"


class JournalLineModel:
    """Modèle de ligne d'écriture"""
    
    def __init__(
        self,
        id: int,
        entry_id: int,
        account_id: int,
        debit: float = 0,
        credit: float = 0,
        description: Optional[str] = None,
        reference: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.entry_id = entry_id
        self.account_id = account_id
        self.debit = debit
        self.credit = credit
        self.description = description
        self.reference = reference
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "entry_id": self.entry_id,
            "account_id": self.account_id,
            "debit": self.debit,
            "credit": self.credit,
            "description": self.description,
            "reference": self.reference,
            "created_at": self.created_at
        }
    
    def is_debit(self) -> bool:
        """Vérifie si débit"""
        return self.debit > 0
    
    def is_credit(self) -> bool:
        """Vérifie si crédit"""
        return self.credit > 0
    
    def amount(self) -> float:
        """Montant"""
        return self.debit if self.debit > 0 else self.credit
