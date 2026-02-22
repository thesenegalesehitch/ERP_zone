"""
Modèle de données pour les opérations bancaires

Ce module définit le modèle de données pour les opérations
dans le module de gestion de la banque.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class OperationModel:
    """Modèle d'opération bancaire"""
    
    def __init__(
        self,
        id: int,
        account_id: int,
        operation_type: str,
        amount: float = 0,
        currency: str = "XOF",
        balance_before: float = 0,
        balance_after: float = 0,
        operation_date: date = None,
        description: Optional[str] = None,
        reference: Optional[str] = None,
        counterparty: Optional[str] = None,
        status: str = "complete",
        channel: str = "guichet",
        executed_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.account_id = account_id
        self.operation_type = operation_type
        self.amount = amount
        self.currency = currency
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.operation_date = operation_date or date.today()
        self.description = description
        self.reference = reference
        self.counterparty = counterparty
        self.status = status
        self.channel = channel
        self.executed_by = executed_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "account_id": self.account_id,
            "operation_type": self.operation_type,
            "amount": self.amount,
            "currency": self.currency,
            "balance_before": self.balance_before,
            "balance_after": self.balance_after,
            "operation_date": self.operation_date,
            "description": self.description,
            "reference": self.reference,
            "counterparty": self.counterparty,
            "status": self.status,
            "channel": self.channel,
            "executed_by": self.executed_by,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "OperationModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            account_id=data.get("account_id"),
            operation_type=data.get("operation_type"),
            amount=data.get("amount", 0),
            currency=data.get("currency", "XOF"),
            balance_before=data.get("balance_before", 0),
            balance_after=data.get("balance_after", 0),
            operation_date=data.get("operation_date"),
            description=data.get("description"),
            reference=data.get("reference"),
            counterparty=data.get("counterparty"),
            status=data.get("status", "complete"),
            channel=data.get("channel", "guichet"),
            executed_by=data.get("executed_by"),
            created_at=data.get("created_at")
        )
    
    def is_credit(self) -> bool:
        """Vérifie si crédit"""
        return self.operation_type in ["depot", "virement_recu", "versement"]
    
    def is_debit(self) -> bool:
        """Vérifie si débit"""
        return self.operation_type in ["retrait", "virement_envoye", "paiement"]


class TransferModel:
    """Modèle de virement"""
    
    def __init__(
        self,
        id: int,
        from_account_id: int,
        to_account_id: int,
        amount: float = 0,
        currency: str = "XOF",
        reference: str = None,
        status: str = "en_attente",
        transfer_date: date = None,
        execution_date: Optional[date] = None,
        reason: Optional[str] = None,
        fees: float = 0,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount
        self.currency = currency
        self.reference = reference
        self.status = status
        self.transfer_date = transfer_date or date.today()
        self.execution_date = execution_date
        self.reason = reason
        self.fees = fees
        self.created_by = created_by
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
            "reference": self.reference,
            "status": self.status,
            "transfer_date": self.transfer_date,
            "execution_date": self.execution_date,
            "reason": self.reason,
            "fees": self.fees,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def total_amount(self) -> float:
        """Montant total avec frais"""
        return self.amount + self.fees
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "complete"


class ChequeModel:
    """Modèle de chèque"""
    
    def __init__(
        self,
        id: int,
        cheque_number: str,
        account_id: int,
        beneficiary: str,
        amount: float = 0,
        currency: str = "XOF",
        issue_date: date = None,
        due_date: Optional[date] = None,
        status: str = "en_circulation",
        bank_name: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.cheque_number = cheque_number
        self.account_id = account_id
        self.beneficiary = beneficiary
        self.amount = amount
        self.currency = currency
        self.issue_date = issue_date or date.today()
        self.due_date = due_date
        self.status = status
        self.bank_name = bank_name
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "cheque_number": self.cheque_number,
            "account_id": self.account_id,
            "beneficiary": self.beneficiary,
            "amount": self.amount,
            "currency": self.currency,
            "issue_date": self.issue_date,
            "due_date": self.due_date,
            "status": self.status,
            "bank_name": self.bank_name,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_paid(self) -> bool:
        """Vérifie si payé"""
        return self.status == "paye"
    
    def is_expired(self) -> bool:
        """Vérifie si expiré"""
        if not self.due_date:
            return False
        return date.today() > self.due_date
