"""
Modèle de données pour les paiements clients

Ce module définit le modèle de données pour les paiements
dans le module de gestion des clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class PaymentModel:
    """Modèle de paiement"""
    
    def __init__(
        self,
        id: int,
        payment_number: str,
        client_id: int,
        invoice_id: Optional[int] = None,
        amount: float = 0,
        currency: str = "XOF",
        payment_method: str = "especes",
        status: str = "en_attente",
        payment_date: Optional[date] = None,
        reference: Optional[str] = None,
        bank_name: Optional[str] = None,
        account_number: Optional[str] = None,
        notes: Optional[str] = None,
        recorded_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.payment_number = payment_number
        self.client_id = client_id
        self.invoice_id = invoice_id
        self.amount = amount
        self.currency = currency
        self.payment_method = payment_method
        self.status = status
        self.payment_date = payment_date
        self.reference = reference
        self.bank_name = bank_name
        self.account_number = account_number
        self.notes = notes
        self.recorded_by = recorded_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "payment_number": self.payment_number,
            "client_id": self.client_id,
            "invoice_id": self.invoice_id,
            "amount": self.amount,
            "currency": self.currency,
            "payment_method": self.payment_method,
            "status": self.status,
            "payment_date": self.payment_date,
            "reference": self.reference,
            "bank_name": self.bank_name,
            "account_number": self.account_number,
            "notes": self.notes,
            "recorded_by": self.recorded_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PaymentModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            payment_number=data.get("payment_number"),
            client_id=data.get("client_id"),
            invoice_id=data.get("invoice_id"),
            amount=data.get("amount", 0),
            currency=data.get("currency", "XOF"),
            payment_method=data.get("payment_method", "especes"),
            status=data.get("status", "en_attente"),
            payment_date=data.get("payment_date"),
            reference=data.get("reference"),
            bank_name=data.get("bank_name"),
            account_number=data.get("account_number"),
            notes=data.get("notes"),
            recorded_by=data.get("recorded_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si complété"""
        return self.status == "complete"
    
    def is_pending(self) -> bool:
        """Vérifie si en attente"""
        return self.status == "en_attente"


class PaymentReminderModel:
    """Modèle de rappel de paiement"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        invoice_id: int,
        reminder_number: int,
        scheduled_date: date,
        sent_date: Optional[date] = None,
        status: str = "planifie",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.invoice_id = invoice_id
        self.reminder_number = reminder_number
        self.scheduled_date = scheduled_date
        self.sent_date = sent_date
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "invoice_id": self.invoice_id,
            "reminder_number": self.reminder_number,
            "scheduled_date": self.scheduled_date,
            "sent_date": self.sent_date,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_sent(self) -> bool:
        """Vérifie si envoyé"""
        return self.status == "envoye"


class CreditNoteModel:
    """Modèle d'avoir"""
    
    def __init__(
        self,
        id: int,
        credit_note_number: str,
        client_id: int,
        invoice_id: Optional[int] = None,
        amount: float = 0,
        currency: str = "XOF",
        reason: Optional[str] = None,
        status: str = "brouillon",
        issue_date: date = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.credit_note_number = credit_note_number
        self.client_id = client_id
        self.invoice_id = invoice_id
        self.amount = amount
        self.currency = currency
        self.reason = reason
        self.status = status
        self.issue_date = issue_date or date.today()
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "credit_note_number": self.credit_note_number,
            "client_id": self.client_id,
            "invoice_id": self.invoice_id,
            "amount": self.amount,
            "currency": self.currency,
            "reason": self.reason,
            "status": self.status,
            "issue_date": self.issue_date,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
