"""
Modèle de données pour l'approvisionnement

Ce module définit le modèle de données pour la gestion
des approvisionnements dans le module d'approvisionnement.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class PurchaseRequestModel:
    """Modèle de demande d'achat"""
    
    def __init__(
        self,
        id: int,
        request_number: str,
        requester_id: int,
        department_id: int,
        priority: str = "normale",
        status: str = "brouillon",
        request_date: Optional[date] = None,
        expected_date: Optional[date] = None,
        total_amount: float = 0,
        currency: str = "XOF",
        justification: Optional[str] = None,
        notes: Optional[str] = None,
        approved_by: Optional[int] = None,
        approved_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.request_number = request_number
        self.requester_id = requester_id
        self.department_id = department_id
        self.priority = priority
        self.status = status
        self.request_date = request_date
        self.expected_date = expected_date
        self.total_amount = total_amount
        self.currency = currency
        self.justification = justification
        self.notes = notes
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "request_number": self.request_number,
            "requester_id": self.requester_id,
            "department_id": self.department_id,
            "priority": self.priority,
            "status": self.status,
            "request_date": self.request_date,
            "expected_date": self.expected_date,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "justification": self.justification,
            "notes": self.notes,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PurchaseRequestModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            request_number=data.get("request_number"),
            requester_id=data.get("requester_id"),
            department_id=data.get("department_id"),
            priority=data.get("priority", "normale"),
            status=data.get("status", "brouillon"),
            request_date=data.get("request_date"),
            expected_date=data.get("expected_date"),
            total_amount=data.get("total_amount", 0),
            currency=data.get("currency", "XOF"),
            justification=data.get("justification"),
            notes=data.get("notes"),
            approved_by=data.get("approved_by"),
            approved_at=data.get("approved_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_approved(self) -> bool:
        """Vérifie si la demande est approuvée"""
        return self.status == "approuve"
    
    def is_pending(self) -> bool:
        """Vérifie si la demande est en attente"""
        return self.status in ["soumis", "en_attente"]


class PurchaseOrderModel:
    """Modèle de bon de commande"""
    
    def __init__(
        self,
        id: int,
        order_number: str,
        supplier_id: int,
        purchase_request_id: Optional[int] = None,
        order_date: Optional[date] = None,
        expected_delivery: Optional[date] = None,
        actual_delivery: Optional[date] = None,
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
        self.purchase_request_id = purchase_request_id
        self.order_date = order_date
        self.expected_delivery = expected_delivery
        self.actual_delivery = actual_delivery
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
            "purchase_request_id": self.purchase_request_id,
            "order_date": self.order_date,
            "expected_delivery": self.expected_delivery,
            "actual_delivery": self.actual_delivery,
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
    
    def calculate_total(self):
        """Calcule le montant total"""
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount
    
    def is_delivered(self) -> bool:
        """Vérifie si la commande est livrée"""
        return self.status == "livre"
    
    def is_overdue(self) -> bool:
        """Vérifie si la commande est en retard"""
        if self.actual_delivery or not self.expected_delivery:
            return False
        return date.today() > self.expected_delivery


class PurchaseOrderLineModel:
    """Modèle de ligne de bon de commande"""
    
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
        """Calcule le total de la ligne"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_rate / 100)
        return subtotal - discount
    
    def is_fully_received(self) -> bool:
        """Vérifie si la quantité complète est reçue"""
        return self.received_quantity >= self.quantity


class DeliveryReceiptModel:
    """Modèle de bordereau de livraison"""
    
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
