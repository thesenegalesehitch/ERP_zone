"""
Modèle de données pour les transactions

Ce module définit le modèle de données pour les transactions
dans le module bancaire.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class TransactionModel:
    """Modèle de transaction"""
    
    def __init__(
        self,
        id: int,
        transaction_number: str,
        account_id: int,
        transaction_type: str,
        amount: float = 0,
        currency: str = "XOF",
        balance_before: float = 0,
        balance_after: float = 0,
        description: Optional[str] = None,
        reference: Optional[str] = None,
        status: str = "complete",
        transaction_date: datetime = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.transaction_number = transaction_number
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.currency = currency
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.description = description
        self.reference = reference
        self.status = status
        self.transaction_date = transaction_date
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transaction_number": self.transaction_number,
            "account_id": self.account_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "currency": self.currency,
            "balance_before": self.balance_before,
            "balance_after": self.balance_after,
            "description": self.description,
            "reference": self.reference,
            "status": self.status,
            "transaction_date": self.transaction_date,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TransactionModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            transaction_number=data.get("transaction_number"),
            account_id=data.get("account_id"),
            transaction_type=data.get("transaction_type"),
            amount=data.get("amount", 0),
            currency=data.get("currency", "XOF"),
            balance_before=data.get("balance_before", 0),
            balance_after=data.get("balance_after", 0),
            description=data.get("description"),
            reference=data.get("reference"),
            status=data.get("status", "complete"),
            transaction_date=data.get("transaction_date"),
            created_at=data.get("created_at")
        )
    
    def is_credit(self) -> bool:
        """Vérifie si crédit"""
        return self.transaction_type in ["depot", "virement_recu", "versement"]
    
    def is_debit(self) -> bool:
        """Vérifie si débit"""
        return self.transaction_type in ["retrait", "virement_envoye", "paiement"]


class TransferModel:
    """Modèle de transfert"""
    
    def __init__(
        self,
        id: int,
        transfer_number: str,
        from_account_id: int,
        to_account_id: int,
        amount: float = 0,
        currency: str = "XOF",
        transfer_type: str = "interne",
        status: str = "en_attente",
        reference: Optional[str] = None,
        description: Optional[str] = None,
        initiated_by: int = None,
        approved_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.transfer_number = transfer_number
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount
        self.currency = currency
        self.transfer_type = transfer_type
        self.status = status
        self.reference = reference
        self.description = description
        self.initiated_by = initiated_by
        self.approved_by = approved_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transfer_number": self.transfer_number,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "amount": self.amount,
            "currency": self.currency,
            "transfer_type": self.transfer_type,
            "status": self.status,
            "reference": self.reference,
            "description": self.description,
            "initiated_by": self.initiated_by,
            "approved_by": self.approved_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "termine"


class StandingOrderModel:
    """Modèle d'ordre permanent"""
    
    def __init__(
        self,
        id: int,
        from_account_id: int,
        to_account_id: int,
        amount: float = 0,
        currency: str = "XOF",
        frequency: str = "mensuel",
        start_date: datetime = None,
        end_date: Optional[datetime] = None,
        status: str = "actif",
        next_execution: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount
        self.currency = currency
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.next_execution = next_execution
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "amount": self.amount,
            "currency": self.currency,
            "frequency": self.frequency,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "next_execution": self.next_execution,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"
