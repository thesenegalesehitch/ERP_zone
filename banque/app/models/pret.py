"""
Modèle de données pour les prêts bancaires

Ce module définit le modèle de données pour les prêts
dans le module de gestion de la banque.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class LoanModel:
    """Modèle de prêt"""
    
    def __init__(
        self,
        id: int,
        loan_number: str,
        client_id: int,
        account_id: int,
        loan_type: str = "personnel",
        amount: float = 0,
        currency: str = "XOF",
        interest_rate: float = 0,
        term_months: int = 12,
        status: str = "en_attente",
        request_date: date = None,
        approval_date: Optional[date] = None,
        disbursement_date: Optional[date] = None,
        first_payment_date: Optional[date] = None,
        purpose: Optional[str] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.loan_number = loan_number
        self.client_id = client_id
        self.account_id = account_id
        self.loan_type = loan_type
        self.amount = amount
        self.currency = currency
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.status = status
        self.request_date = request_date or date.today()
        self.approval_date = approval_date
        self.disbursement_date = disbursement_date
        self.first_payment_date = first_payment_date
        self.purpose = purpose
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "loan_number": self.loan_number,
            "client_id": self.client_id,
            "account_id": self.account_id,
            "loan_type": self.loan_type,
            "amount": self.amount,
            "currency": self.currency,
            "interest_rate": self.interest_rate,
            "term_months": self.term_months,
            "status": self.status,
            "request_date": self.request_date,
            "approval_date": self.approval_date,
            "disbursement_date": self.disbursement_date,
            "first_payment_date": self.first_payment_date,
            "purpose": self.purpose,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LoanModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            loan_number=data.get("loan_number"),
            client_id=data.get("client_id"),
            account_id=data.get("account_id"),
            loan_type=data.get("loan_type", "personnel"),
            amount=data.get("amount", 0),
            currency=data.get("currency", "XOF"),
            interest_rate=data.get("interest_rate", 0),
            term_months=data.get("term_months", 12),
            status=data.get("status", "en_attente"),
            request_date=data.get("request_date"),
            approval_date=data.get("approval_date"),
            disbursement_date=data.get("disbursement_date"),
            first_payment_date=data.get("first_payment_date"),
            purpose=data.get("purpose"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def total_interest(self) -> float:
        """Intérêt total"""
        return self.amount * (self.interest_rate / 100)
    
    def total_amount(self) -> float:
        """Montant total à remboursé"""
        return self.amount + self.total_interest()
    
    def monthly_payment(self) -> float:
        """Mensualité"""
        if self.term_months == 0:
            return 0
        return self.total_amount() / self.term_months
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"


class LoanPaymentModel:
    """Modèle de paiement de prêt"""
    
    def __init__(
        self,
        id: int,
        loan_id: int,
        payment_number: int,
        amount: float = 0,
        currency: str = "XOF",
        principal: float = 0,
        interest: float = 0,
        balance_before: float = 0,
        balance_after: float = 0,
        payment_date: date = None,
        status: str = "en_attente",
        payment_method: Optional[str] = None,
        reference: Optional[str] = None,
        notes: Optional[str] = None,
        recorded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.loan_id = loan_id
        self.payment_number = payment_number
        self.amount = amount
        self.currency = currency
        self.principal = principal
        self.interest = interest
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.payment_date = payment_date or date.today()
        self.status = status
        self.payment_method = payment_method
        self.reference = reference
        self.notes = notes
        self.recorded_by = recorded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "loan_id": self.loan_id,
            "payment_number": self.payment_number,
            "amount": self.amount,
            "currency": self.currency,
            "principal": self.principal,
            "interest": self.interest,
            "balance_before": self.balance_before,
            "balance_after": self.balance_after,
            "payment_date": self.payment_date,
            "status": self.status,
            "payment_method": self.payment_method,
            "reference": self.reference,
            "notes": self.notes,
            "recorded_by": self.recorded_by,
            "created_at": self.created_at
        }
    
    def is_paid(self) -> bool:
        """Vérifie si payé"""
        return self.status == "paye"


class LoanGuaranteeModel:
    """Modèle de garantie de prêt"""
    
    def __init__(
        self,
        id: int,
        loan_id: int,
        guarantee_type: str,
        description: str,
        value: float = 0,
        currency: str = "XOF",
        status: str = "actif",
        document_url: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.loan_id = loan_id
        self.guarantee_type = guarantee_type
        self.description = description
        self.value = value
        self.currency = currency
        self.status = status
        self.document_url = document_url
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "loan_id": self.loan_id,
            "guarantee_type": self.guarantee_type,
            "description": self.description,
            "value": self.value,
            "currency": self.currency,
            "status": self.status,
            "document_url": self.document_url,
            "notes": self.notes,
            "created_at": self.created_at
        }
