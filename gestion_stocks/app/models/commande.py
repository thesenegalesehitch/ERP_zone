"""
Modèle de données pour les commandes de stock

Ce module définit le modèle de données pour les commandes
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class OrderModel:
    """Modèle de commande"""
    
    def __init__(
        self,
        id: int,
        order_number: str,
        supplier_id: int,
        warehouse_id: int,
        order_type: str = "achat",
        status: str = "en_attente",
        order_date: date = None,
        expected_date: Optional[date] = None,
        received_date: Optional[date] = None,
        total_amount: float = 0,
        currency: str = "XOF",
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_number = order_number
        self.supplier_id = supplier_id
        self.warehouse_id = warehouse_id
        self.order_type = order_type
        self.status = status
        self.order_date = order_date or date.today()
        self.expected_date = expected_date
        self.received_date = received_date
        self.total_amount = total_amount
        self.currency = currency
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "supplier_id": self.supplier_id,
            "warehouse_id": self.warehouse_id,
            "order_type": self.order_type,
            "status": self.status,
            "order_date": self.order_date,
            "expected_date": self.expected_date,
            "received_date": self.received_date,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "OrderModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            order_number=data.get("order_number"),
            supplier_id=data.get("supplier_id"),
            warehouse_id=data.get("warehouse_id"),
            order_type=data.get("order_type", "achat"),
            status=data.get("status", "en_attente"),
            order_date=data.get("order_date"),
            expected_date=data.get("expected_date"),
            received_date=data.get("received_date"),
            total_amount=data.get("total_amount", 0),
            currency=data.get("currency", "XOF"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si terminée"""
        return self.status == "recue"
    
    def is_pending(self) -> bool:
        """Vérifie si en attente"""
        return self.status == "en_attente"


class OrderItemModel:
    """Modèle d'article de commande"""
    
    def __init__(
        self,
        id: int,
        order_id: int,
        product_id: int,
        quantity: float = 0,
        unit_price: float = 0,
        currency: str = "XOF",
        quantity_received: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.currency = currency
        self.quantity_received = quantity_received
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "currency": self.currency,
            "quantity_received": self.quantity_received,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def total_price(self) -> float:
        """Prix total"""
        return self.quantity * self.unit_price
    
    def is_fully_received(self) -> bool:
        """Vérifie si entièrement reçu"""
        return self.quantity_received >= self.quantity


class OrderDeliveryModel:
    """Modèle de livraison de commande"""
    
    def __init__(
        self,
        id: int,
        order_id: int,
        delivery_number: str,
        delivery_date: date = None,
        status: str = "en_transit",
        carrier: Optional[str] = None,
        tracking_number: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_id = order_id
        self.delivery_number = delivery_number
        self.delivery_date = delivery_date or date.today()
        self.status = status
        self.carrier = carrier
        self.tracking_number = tracking_number
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "delivery_number": self.delivery_number,
            "delivery_date": self.delivery_date,
            "status": self.status,
            "carrier": self.carrier,
            "tracking_number": self.tracking_number,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_delivered(self) -> bool:
        """Vérifie si livré"""
        return self.status == "livre"
