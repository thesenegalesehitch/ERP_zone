"""
Modèle de données pour les devis

Ce module définit le modèle de données pour les devis
dans le module de gestion des clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class QuoteModel:
    """Modèle de devis"""
    
    def __init__(
        self,
        id: int,
        quote_number: str,
        client_id: int,
        quote_date: Optional[date] = None,
        valid_until: Optional[date] = None,
        subtotal: float = 0,
        tax_amount: float = 0,
        discount_amount: float = 0,
        total_amount: float = 0,
        currency: str = "XOF",
        status: str = "brouillon",
        notes: Optional[str] = None,
        terms: Optional[str] = None,
        created_by: int = None,
        sent_at: Optional[datetime] = None,
        accepted_at: Optional[datetime] = None,
        rejected_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.quote_number = quote_number
        self.client_id = client_id
        self.quote_date = quote_date
        self.valid_until = valid_until
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.total_amount = total_amount
        self.currency = currency
        self.status = status
        self.notes = notes
        self.terms = terms
        self.created_by = created_by
        self.sent_at = sent_at
        self.accepted_at = accepted_at
        self.rejected_at = rejected_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "quote_number": self.quote_number,
            "client_id": self.client_id,
            "quote_date": self.quote_date,
            "valid_until": self.valid_until,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "status": self.status,
            "notes": self.notes,
            "terms": self.terms,
            "created_by": self.created_by,
            "sent_at": self.sent_at,
            "accepted_at": self.accepted_at,
            "rejected_at": self.rejected_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "QuoteModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            quote_number=data.get("quote_number"),
            client_id=data.get("client_id"),
            quote_date=data.get("quote_date"),
            valid_until=data.get("valid_until"),
            subtotal=data.get("subtotal", 0),
            tax_amount=data.get("tax_amount", 0),
            discount_amount=data.get("discount_amount", 0),
            total_amount=data.get("total_amount", 0),
            currency=data.get("currency", "XOF"),
            status=data.get("status", "brouillon"),
            notes=data.get("notes"),
            terms=data.get("terms"),
            created_by=data.get("created_by"),
            sent_at=data.get("sent_at"),
            accepted_at=data.get("accepted_at"),
            rejected_at=data.get("rejected_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_total(self):
        """Calcule le montant total"""
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
    
    def is_sent(self) -> bool:
        """Vérifie si le devis est envoyé"""
        return self.sent_at is not None
    
    def is_accepted(self) -> bool:
        """Vérifie si le devis est accepté"""
        return self.status == "accepte"
    
    def is_expired(self) -> bool:
        """Vérifie si le devis est expiré"""
        if not self.valid_until:
            return False
        return date.today() > self.valid_until


class QuoteLineModel:
    """Modèle de ligne de devis"""
    
    def __init__(
        self,
        id: int,
        quote_id: int,
        product_id: Optional[int] = None,
        description: Optional[str] = None,
        quantity: float = 1,
        unit_price: float = 0,
        tax_rate: float = 0,
        discount_rate: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.quote_id = quote_id
        self.product_id = product_id
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.tax_rate = tax_rate
        self.discount_rate = discount_rate
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "quote_id": self.quote_id,
            "product_id": self.product_id,
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "tax_rate": self.tax_rate,
            "discount_rate": self.discount_rate,
            "created_at": self.created_at
        }
    
    def calculate_total(self) -> float:
        """Calcule le total de la ligne"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_rate / 100)
        return subtotal - discount


class QuoteVersionModel:
    """Modèle de version de devis"""
    
    def __init__(
        self,
        id: int,
        quote_id: int,
        version_number: int,
        total_amount: float = 0,
        changes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.quote_id = quote_id
        self.version_number = version_number
        self.total_amount = total_amount
        self.changes = changes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "quote_id": self.quote_id,
            "version_number": self.version_number,
            "total_amount": self.total_amount,
            "changes": self.changes,
            "created_at": self.created_at
        }
