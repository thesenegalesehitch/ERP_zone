"""
Modèle de données pour les factures

Ce module définit le modèle de données pour les factures
dans le module de comptabilité.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class InvoiceModel:
    """Modèle de facture"""
    
    def __init__(
        self,
        id: int,
        invoice_number: str,
        customer_id: int,
        invoice_date: date = None,
        due_date: date = None,
        subtotal: float = 0,
        tax_amount: float = 0,
        discount_amount: float = 0,
        shipping_cost: float = 0,
        total_amount: float = 0,
        amount_paid: float = 0,
        currency: str = "XOF",
        status: str = "brouillon",
        payment_terms: Optional[str] = None,
        notes: Optional[str] = None,
        terms: Optional[str] = None,
        sent_at: Optional[datetime] = None,
        paid_at: Optional[datetime] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.invoice_number = invoice_number
        self.customer_id = customer_id
        self.invoice_date = invoice_date
        self.due_date = due_date
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.shipping_cost = shipping_cost
        self.total_amount = total_amount
        self.amount_paid = amount_paid
        self.currency = currency
        self.status = status
        self.payment_terms = payment_terms
        self.notes = notes
        self.terms = terms
        self.sent_at = sent_at
        self.paid_at = paid_at
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "customer_id": self.customer_id,
            "invoice_date": self.invoice_date,
            "due_date": self.due_date,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "shipping_cost": self.shipping_cost,
            "total_amount": self.total_amount,
            "amount_paid": self.amount_paid,
            "currency": self.currency,
            "status": self.status,
            "payment_terms": self.payment_terms,
            "notes": self.notes,
            "terms": self.terms,
            "sent_at": self.sent_at,
            "paid_at": self.paid_at,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "InvoiceModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            invoice_number=data.get("invoice_number"),
            customer_id=data.get("customer_id"),
            invoice_date=data.get("invoice_date"),
            due_date=data.get("due_date"),
            subtotal=data.get("subtotal", 0),
            tax_amount=data.get("tax_amount", 0),
            discount_amount=data.get("discount_amount", 0),
            shipping_cost=data.get("shipping_cost", 0),
            total_amount=data.get("total_amount", 0),
            amount_paid=data.get("amount_paid", 0),
            currency=data.get("currency", "XOF"),
            status=data.get("status", "brouillon"),
            payment_terms=data.get("payment_terms"),
            notes=data.get("notes"),
            terms=data.get("terms"),
            sent_at=data.get("sent_at"),
            paid_at=data.get("paid_at"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_total(self):
        """Calcule le montant total"""
        self.total_amount = (self.subtotal + self.tax_amount + 
                           self.shipping_cost - self.discount_amount)
    
    def balance_due(self) -> float:
        """Calcule le solde dû"""
        return self.total_amount - self.amount_paid
    
    def is_paid(self) -> bool:
        """Vérifie si payé"""
        return self.amount_paid >= self.total_amount
    
    def is_overdue(self) -> bool:
        """Vérifie si en retard"""
        if not self.due_date or self.is_paid():
            return False
        return date.today() > self.due_date


class InvoiceLineModel:
    """Modèle de ligne de facture"""
    
    def __init__(
        self,
        id: int,
        invoice_id: int,
        product_id: Optional[int] = None,
        description: Optional[str] = None,
        quantity: float = 1,
        unit_price: float = 0,
        tax_rate: float = 0,
        discount_rate: float = 0,
        line_total: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.invoice_id = invoice_id
        self.product_id = product_id
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.tax_rate = tax_rate
        self.discount_rate = discount_rate
        self.line_total = line_total
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "product_id": self.product_id,
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "tax_rate": self.tax_rate,
            "discount_rate": self.discount_rate,
            "line_total": self.line_total,
            "created_at": self.created_at
        }
    
    def calculate_line_total(self):
        """Calcule le total de la ligne"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_rate / 100)
        self.line_total = subtotal - discount


class PaymentModel:
    """Modèle de paiement"""
    
    def __init__(
        self,
        id: int,
        invoice_id: int,
        payment_number: str,
        amount: float = 0,
        currency: str = "XOF",
        payment_method: str = "virement",
        payment_date: date = None,
        reference: Optional[str] = None,
        status: str = "en_attente",
        notes: Optional[str] = None,
        processed_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.invoice_id = invoice_id
        self.payment_number = payment_number
        self.amount = amount
        self.currency = currency
        self.payment_method = payment_method
        self.payment_date = payment_date
        self.reference = reference
        self.status = status
        self.notes = notes
        self.processed_at = processed_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "payment_number": self.payment_number,
            "amount": self.amount,
            "currency": self.currency,
            "payment_method": self.payment_method,
            "payment_date": self.payment_date,
            "reference": self.reference,
            "status": self.status,
            "notes": self.notes,
            "processed_at": self.processed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_processed(self) -> bool:
        """Vérifie si traité"""
        return self.status == "traite"
