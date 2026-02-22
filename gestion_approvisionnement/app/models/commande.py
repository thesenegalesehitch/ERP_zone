"""
Modèle de données pour les commandes

Ce module définit le modèle de données pour les commandes
dans le module de gestion des approvisionnements.

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
        actual_delivery: Optional[date] = None,
        subtotal: float = 0,
        tax_amount: float = 0,
        discount_amount: float = 0,
        total_amount: float = 0,
        currency: str = "XOF",
        status: str = "brouillon",
        payment_status: str = "non_paye",
        payment_method: Optional[str] = None,
        notes: Optional[str] = None,
        terms: Optional[str] = None,
        created_by: int = None,
        approved_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_number = order_number
        self.supplier_id = supplier_id
        self.order_date = order_date
        self.expected_delivery = expected_delivery
        self.actual_delivery = actual_delivery
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.total_amount = total_amount
        self.currency = currency
        self.status = status
        self.payment_status = payment_status
        self.payment_method = payment_method
        self.notes = notes
        self.terms = terms
        self.created_by = created_by
        self.approved_by = approved_by
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
            "actual_delivery": self.actual_delivery,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "status": self.status,
            "payment_status": self.payment_status,
            "payment_method": self.payment_method,
            "notes": self.notes,
            "terms": self.terms,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
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
            actual_delivery=data.get("actual_delivery"),
            subtotal=data.get("subtotal", 0),
            tax_amount=data.get("tax_amount", 0),
            discount_amount=data.get("discount_amount", 0),
            total_amount=data.get("total_amount", 0),
            currency=data.get("currency", "XOF"),
            status=data.get("status", "brouillon"),
            payment_status=data.get("payment_status", "non_paye"),
            payment_method=data.get("payment_method"),
            notes=data.get("notes"),
            terms=data.get("terms"),
            created_by=data.get("created_by"),
            approved_by=data.get("approved_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_total(self):
        """Calcule le montant total"""
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
    
    def is_approved(self) -> bool:
        """Vérifie si la commande est approuvée"""
        return self.status == "approuve"
    
    def is_received(self) -> bool:
        """Vérifie si la commande est reçue"""
        return self.status == "recue"


class PurchaseOrderLineModel:
    """Modèle de ligne de commande"""
    
    def __init__(
        self,
        id: int,
        order_id: int,
        product_id: int,
        description: Optional[str] = None,
        quantity: int = 1,
        unit_price: float = 0,
        tax_rate: float = 0,
        discount_rate: float = 0,
        received_quantity: int = 0,
        rejected_quantity: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.tax_rate = tax_rate
        self.discount_rate = discount_rate
        self.received_quantity = received_quantity
        self.rejected_quantity = rejected_quantity
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "tax_rate": self.tax_rate,
            "discount_rate": self.discount_rate,
            "received_quantity": self.received_quantity,
            "rejected_quantity": self.rejected_quantity,
            "created_at": self.created_at
        }
    
    def calculate_total(self) -> float:
        """Calcule le total de la ligne"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_rate / 100)
        return subtotal - discount
    
    def is_fully_received(self) -> bool:
        """Vérifie si la quantité est entièrement reçue"""
        return self.received_quantity >= self.quantity


class DeliveryReceiptModel:
    """Modèle de bon de livraison"""
    
    def __init__(
        self,
        id: int,
        receipt_number: str,
        order_id: int,
        receipt_date: Optional[date] = None,
        status: str = "en_attente",
        received_by: int = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.receipt_number = receipt_number
        self.order_id = order_id
        self.receipt_date = receipt_date
        self.status = status
        self.received_by = received_by
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "receipt_number": self.receipt_number,
            "order_id": self.order_id,
            "receipt_date": self.receipt_date,
            "status": self.status,
            "received_by": self.received_by,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_received(self) -> bool:
        """Vérifie si la livraison est reçue"""
        return self.status == "recue"


class RequestForQuotationModel:
    """Modèle de demande de devis"""
    
    def __init__(
        self,
        id: int,
        rfq_number: str,
        title: str,
        supplier_id: Optional[int] = None,
        request_date: Optional[date] = None,
        deadline: Optional[date] = None,
        status: str = "nouveau",
        description: Optional[str] = None,
        terms: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.rfq_number = rfq_number
        self.title = title
        self.supplier_id = supplier_id
        self.request_date = request_date
        self.deadline = deadline
        self.status = status
        self.description = description
        self.terms = terms
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "rfq_number": self.rfq_number,
            "title": self.title,
            "supplier_id": self.supplier_id,
            "request_date": self.request_date,
            "deadline": self.deadline,
            "status": self.status,
            "description": self.description,
            "terms": self.terms,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
