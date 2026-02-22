"""
Modèle de données pour les livraisons

Ce module définit le modèle de données pour les livraisons
dans le module de gestion des approvisionnements.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class DeliveryModel:
    """Modèle de livraison"""
    
    def __init__(
        self,
        id: int,
        delivery_number: str,
        purchase_order_id: int,
        delivery_date: Optional[date] = None,
        received_by: int = None,
        status: str = "en_attente",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.delivery_number = delivery_number
        self.purchase_order_id = purchase_order_id
        self.delivery_date = delivery_date
        self.received_by = received_by
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "delivery_number": self.delivery_number,
            "purchase_order_id": self.purchase_order_id,
            "delivery_date": self.delivery_date,
            "received_by": self.received_by,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DeliveryModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            delivery_number=data.get("delivery_number"),
            purchase_order_id=data.get("purchase_order_id"),
            delivery_date=data.get("delivery_date"),
            received_by=data.get("received_by"),
            status=data.get("status", "en_attente"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_received(self) -> bool:
        """Vérifie si la livraison est reçue"""
        return self.status == "recue"


class DeliveryLineModel:
    """Modèle de ligne de livraison"""
    
    def __init__(
        self,
        id: int,
        delivery_id: int,
        product_id: int,
        ordered_quantity: int = 0,
        delivered_quantity: int = 0,
        accepted_quantity: int = 0,
        rejected_quantity: int = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.delivery_id = delivery_id
        self.product_id = product_id
        self.ordered_quantity = ordered_quantity
        self.delivered_quantity = delivered_quantity
        self.accepted_quantity = accepted_quantity
        self.rejected_quantity = rejected_quantity
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "delivery_id": self.delivery_id,
            "product_id": self.product_id,
            "ordered_quantity": self.ordered_quantity,
            "delivered_quantity": self.delivered_quantity,
            "accepted_quantity": self.accepted_quantity,
            "rejected_quantity": self.rejected_quantity,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_complete(self) -> bool:
        """Vérifie si la livraison est complète"""
        return self.accepted_quantity + self.rejected_quantity >= self.delivered_quantity


class GoodsReceiptNoteModel:
    """Modèle de bon de réception"""
    
    def __init__(
        self,
        id: int,
        grn_number: str,
        supplier_id: int,
        receipt_date: Optional[date] = None,
        total_items: int = 0,
        total_quantity: int = 0,
        status: str = "en_cours",
        notes: Optional[str] = None,
        inspected_by: Optional[int] = None,
        approved_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.grn_number = grn_number
        self.supplier_id = supplier_id
        self.receipt_date = receipt_date
        self.total_items = total_items
        self.total_quantity = total_quantity
        self.status = status
        self.notes = notes
        self.inspected_by = inspected_by
        self.approved_by = approved_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "grn_number": self.grn_number,
            "supplier_id": self.supplier_id,
            "receipt_date": self.receipt_date,
            "total_items": self.total_items,
            "total_quantity": self.total_quantity,
            "status": self.status,
            "notes": self.notes,
            "inspected_by": self.inspected_by,
            "approved_by": self.approved_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si la réception est terminée"""
        return self.status == "termine"


class ReturnModel:
    """Modèle de retour"""
    
    def __init__(
        self,
        id: int,
        return_number: str,
        purchase_order_id: int,
        return_type: str = "fournisseur",
        reason: Optional[str] = None,
        return_date: Optional[date] = None,
        status: str = "en_attente",
        total_amount: float = 0,
        notes: Optional[str] = None,
        approved_by: Optional[int] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.return_number = return_number
        self.purchase_order_id = purchase_order_id
        self.return_type = return_type
        self.reason = reason
        self.return_date = return_date
        self.status = status
        self.total_amount = total_amount
        self.notes = notes
        self.approved_by = approved_by
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "return_number": self.return_number,
            "purchase_order_id": self.purchase_order_id,
            "return_type": self.return_type,
            "reason": self.reason,
            "return_date": self.return_date,
            "status": self.status,
            "total_amount": self.total_amount,
            "notes": self.notes,
            "approved_by": self.approved_by,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_approved(self) -> bool:
        """Vérifie si le retour est approuvé"""
        return self.status == "approuve"
    
    def is_completed(self) -> bool:
        """Vérifie si le retour est terminé"""
        return self.status == "termine"
