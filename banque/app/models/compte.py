"""
Modèle de données pour les comptes bancaires

Ce module définit le modèle de données pour les comptes bancaires
dans le module de gestion de la banque.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class AccountModel:
    """Modèle de compte bancaire"""
    
    def __init__(
        self,
        id: int,
        account_number: str,
        account_type: str = "courant",
        client_id: int,
        balance: float = 0,
        currency: str = "XOF",
        status: str = "actif",
        opening_date: date = None,
        closing_date: Optional[date] = None,
        overdraft_limit: float = 0,
        interest_rate: float = 0,
        branch: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.account_number = account_number
        self.account_type = account_type
        self.client_id = client_id
        self.balance = balance
        self.currency = currency
        self.status = status
        self.opening_date = opening_date or date.today()
        self.closing_date = closing_date
        self.overdraft_limit = overdraft_limit
        self.interest_rate = interest_rate
        self.branch = branch
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "account_number": self.account_number,
            "account_type": self.account_type,
            "client_id": self.client_id,
            "balance": self.balance,
            "currency": self.currency,
            "status": self.status,
            "opening_date": self.opening_date,
            "closing_date": self.closing_date,
            "overdraft_limit": self.overdraft_limit,
            "interest_rate": self.interest_rate,
            "branch": self.branch,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AccountModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            account_number=data.get("account_number"),
            account_type=data.get("account_type", "courant"),
            client_id=data.get("client_id"),
            balance=data.get("balance", 0),
            currency=data.get("currency", "XOF"),
            status=data.get("status", "actif"),
            opening_date=data.get("opening_date"),
            closing_date=data.get("closing_date"),
            overdraft_limit=data.get("overdraft_limit", 0),
            interest_rate=data.get("interest_rate", 0),
            branch=data.get("branch"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"
    
    def can_withdraw(self, amount: float) -> bool:
        """Vérifie si peut retirer"""
        return (self.balance + self.overdraft_limit) >= amount
    
    def available_balance(self) -> bool:
        """Solde disponible"""
        return self.balance + self.overdraft_limit


class SavingsAccountModel:
    """Modèle de compte épargne"""
    
    def __init__(
        self,
        id: int,
        account_id: int,
        interest_rate: float = 2.5,
        minimum_balance: float = 0,
        withdrawal_limit: int = 4,
        withdrawal_count: int = 0,
        last_interest_date: Optional[date] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.account_id = account_id
        self.interest_rate = interest_rate
        self.minimum_balance = minimum_balance
        self.withdrawal_limit = withdrawal_limit
        self.withdrawal_count = withdrawal_count
        self.last_interest_date = last_interest_date
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "account_id": self.account_id,
            "interest_rate": self.interest_rate,
            "minimum_balance": self.minimum_balance,
            "withdrawal_limit": self.withdrawal_limit,
            "withdrawal_count": self.withdrawal_count,
            "last_interest_date": self.last_interest_date,
            "created_at": self.created_at
        }
    
    def can_withdraw(self) -> bool:
        """Vérifie si peut retirer"""
        return self.withdrawal_count < self.withdrawal_limit


class AccountStatementModel:
    """Modèle de relevé de compte"""
    
    def __init__(
        self,
        id: int,
        account_id: int,
        start_date: date,
        end_date: date,
        opening_balance: float = 0,
        closing_balance: float = 0,
        total_credits: float = 0,
        total_debits: float = 0,
        generated_date: date = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.account_id = account_id
        self.start_date = start_date
        self.end_date = end_date
        self.opening_balance = opening_balance
        self.closing_balance = closing_balance
        self.total_credits = total_credits
        self.total_debits = total_debits
        self.generated_date = generated_date or date.today()
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "account_id": self.account_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "opening_balance": self.opening_balance,
            "closing_balance": self.closing_balance,
            "total_credits": self.total_credits,
            "total_debits": self.total_debits,
            "generated_date": self.generated_date,
            "notes": self.notes,
            "created_at": self.created_at
        }
