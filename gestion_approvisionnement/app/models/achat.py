"""
Modèle de données pour les achats

Ce module définit le modèle de données pour les achats
dans le module d'approvisionnement.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class PurchaseOrderModel:
    """Modèle de bon de commande"""
    
    def __init__(
        self,
        id: int,
        order_number: str,
        supplier_id: int,
        order_date: Optional[date] = None,
        expected_delivery: Optional[date] = None,
        subtotal: float = 0,
        tax_amount: float = 0,
        discount_amount: float = 0,
        shipping_cost: float = 0,
        total_amount: float = 0,
        currency: str = "XOF",
        status: str = "brouillon",
        payment_terms: Optional[str] = None,
        delivery_address: Optional[str] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        approved_by: Optional[int] = None,
        approved_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_number = order_number
        self.supplier_id = supplier_id
        self.order_date = order_date
        self.expected_delivery = expected_delivery
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.shipping_cost = shipping_cost
        self.total_amount = total_amount
        self.currency = currency
        self.status = status
        self.payment_terms = payment_terms
        self.delivery_address = delivery_address
        self.notes = notes
        self.created_by = created_by
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "supplier_id": self.supplier_id,
            "order_date": self.order_date,
            "expected_delivery": self.expected_delivery,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "shipping_cost": self.shipping_cost,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "status": self.status,
            "payment_terms": self.payment_terms,
            "delivery_address": self.delivery_address,
            "notes": self.notes,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PurchaseOrderModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            order_number=data.get("order_number"),
            supplier_id=data.get("supplier_id"),
            order_date=data.get("order_date"),
            expected_delivery=data.get("expected_delivery"),
            subtotal=data.get("subtotal", 0),
            tax_amount=data.get("tax_amount", 0),
            discount_amount=data.get("discount_amount", 0),
            shipping_cost=data.get("shipping_cost", 0),
            total_amount=data.get("total_amount", 0),
            currency=data.get("currency", "XOF"),
            status=data.get("status", "brouillon"),
            payment_terms=data.get("payment_terms"),
            delivery_address=data.get("delivery_address"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            approved_by=data.get("approved_by"),
            approved_at=data.get("approved_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_total(self):
        """Calcule le montant total"""
        self.total_amount = (self.subtotal + self.tax_amount + 
                           self.shipping_cost - self.discount_amount)
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"
    
    def is_received(self) -> bool:
        """Vérifie si reçu"""
        return self.status == "recus"


class PurchaseLineModel:
    """Modèle de ligne d'achat"""
    
    def __init__(
        self,
        id: int,
        order_id: int,
        product_id: int,
        quantity: float = 1,
        unit_price: float = 0,
        tax_rate: float = 0,
        discount_rate: float = 0,
        received_quantity: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.tax_rate = tax_rate
        self.discount_rate = discount_rate
        self.received_quantity = received_quantity
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "tax_rate": self.tax_rate,
            "discount_rate": self.discount_rate,
            "received_quantity": self.received_quantity,
            "created_at": self.created_at
        }
    
    def calculate_total(self) -> float:
        """Calcule le total"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_rate / 100)
        return subtotal - discount
    
    def is_fully_received(self) -> bool:
        """Vérifie si entièrement reçu"""
        return self.received_quantity >= self.quantity


class ReceiptModel:
    """Modèle de réception"""
    
    def __init__(
        self,
        id: int,
        receipt_number: str,
        purchase_order_id: int,
        receipt_date: Optional[date] = None,
        received_by: int = None,
        notes: Optional[str] = None,
        status: str = "brouillon",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.receipt_number = receipt_number
        self.purchase_order_id = purchase_order_id
        self.receipt_date = receipt_date
        self.received_by = received_by
        self.notes = notes
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "receipt_number": self.receipt_number,
            "purchase_order_id": self.purchase_order_id,
            "receipt_date": self.receipt_date,
            "received_by": self.received_by,
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "termine"
