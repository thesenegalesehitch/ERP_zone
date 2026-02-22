"""
Modèle de données pour les transactions comptables

Ce module définit le modèle de données pour les transactions
dans le module comptabilité.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class AccountingTransactionModel:
    """Modèle de transaction comptable"""
    
    def __init__(
        self,
        id: int,
        transaction_number: str,
        transaction_date: date,
        transaction_type: str,
        description: Optional[str] = None,
        reference: Optional[str] = None,
        amount: float = 0,
        status: str = "brouillon",
        validated_by: Optional[int] = None,
        validated_at: Optional[datetime] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.transaction_number = transaction_number
        self.transaction_date = transaction_date
        self.transaction_type = transaction_type
        self.description = description
        self.reference = reference
        self.amount = amount
        self.status = status
        self.validated_by = validated_by
        self.validated_at = validated_at
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transaction_number": self.transaction_number,
            "transaction_date": self.transaction_date,
            "transaction_type": self.transaction_type,
            "description": self.description,
            "reference": self.reference,
            "amount": self.amount,
            "status": self.status,
            "validated_by": self.validated_by,
            "validated_at": self.validated_at,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AccountingTransactionModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            transaction_number=data.get("transaction_number"),
            transaction_date=data.get("transaction_date"),
            transaction_type=data.get("transaction_type"),
            description=data.get("description"),
            reference=data.get("reference"),
            amount=data.get("amount", 0),
            status=data.get("status", "brouillon"),
            validated_by=data.get("validated_by"),
            validated_at=data.get("validated_at"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_validated(self) -> bool:
        """Vérifie si la transaction est validée"""
        return self.status == "valide"
    
    def is_posted(self) -> bool:
        """Vérifie si la transaction est passée"""
        return self.status == "passe"


class JournalEntryModel:
    """Modèle d'écriture comptable"""
    
    def __init__(
        self,
        id: int,
        transaction_id: int,
        account_id: int,
        debit: float = 0,
        credit: float = 0,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.debit = debit
        self.credit = credit
        self.description = description
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "debit": self.debit,
            "credit": self.credit,
            "description": self.description,
            "created_at": self.created_at
        }
    
    def is_balanced(self) -> bool:
        """Vérifie si l'écriture est équilibrée"""
        return self.debit == self.credit


class AccountModel:
    """Modèle de compte comptable"""
    
    def __init__(
        self,
        id: int,
        account_number: str,
        account_name: str,
        account_type: str = "actif",
        parent_id: Optional[int] = None,
        balance: float = 0,
        is_active: bool = True,
        allow_transaction: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.account_number = account_number
        self.account_name = account_name
        self.account_type = account_type
        self.parent_id = parent_id
        self.balance = balance
        self.is_active = is_active
        self.allow_transaction = allow_transaction
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
            "balance": self.balance,
            "is_active": self.is_active,
            "allow_transaction": self.allow_transaction,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_debit_balance(self) -> bool:
        """Vérifie si le solde est débit"""
        return self.account_type in ["actif", "charge"]
    
    def is_credit_balance(self) -> bool:
        """Vérifie si le solde est crédit"""
        return self.account_type in ["passif", "produit", "capitaux"]


class InvoiceModel:
    """Modèle de facture"""
    
    def __init__(
        self,
        id: int,
        invoice_number: str,
        invoice_type: str = "client",
        client_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        invoice_date: Optional[date] = None,
        due_date: Optional[date] = None,
        subtotal: float = 0,
        tax_amount: float = 0,
        discount_amount: float = 0,
        total_amount: float = 0,
        status: str = "brouillon",
        paid_amount: float = 0,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.invoice_number = invoice_number
        self.invoice_type = invoice_type
        self.client_id = client_id
        self.supplier_id = supplier_id
        self.invoice_date = invoice_date
        self.due_date = due_date
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.total_amount = total_amount
        self.status = status
        self.paid_amount = paid_amount
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "invoice_type": self.invoice_type,
            "client_id": self.client_id,
            "supplier_id": self.supplier_id,
            "invoice_date": self.invoice_date,
            "due_date": self.due_date,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "status": self.status,
            "paid_amount": self.paid_amount,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_paid(self) -> bool:
        """Vérifie si la facture est payée"""
        return self.paid_amount >= self.total_amount
    
    def balance_due(self) -> float:
        """Retourne le montant restant dû"""
        return self.total_amount - self.paid_amount
    
    def is_overdue(self) -> bool:
        """Vérifie si la facture est en retard"""
        if not self.due_date or self.is_paid():
            return False
        return date.today() > self.due_date


class PaymentModel:
    """Modèle de paiement"""
    
    def __init__(
        self,
        id: int,
        payment_number: str,
        invoice_id: int,
        amount: float,
        payment_method: str,
        payment_date: Optional[date] = None,
        reference: Optional[str] = None,
        status: str = "complete",
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.payment_number = payment_number
        self.invoice_id = invoice_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_date = payment_date
        self.reference = reference
        self.status = status
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "payment_number": self.payment_number,
            "invoice_id": self.invoice_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "payment_date": self.payment_date,
            "reference": self.reference,
            "status": self.status,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at
        }
    
    def is_complete(self) -> bool:
        """Vérifie si le paiement est complet"""
        return self.status == "complete"
