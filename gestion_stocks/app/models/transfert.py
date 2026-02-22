"""
Modèle de données pour les transferts de stock

Ce module définit le modèle de données pour les transferts
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class TransferModel:
    """Modèle de transfert"""
    
    def __init__(
        self,
        id: int,
        transfer_number: str,
        from_warehouse_id: int,
        to_warehouse_id: int,
        status: str = "en_attente",
        request_date: date = None,
        approval_date: Optional[date] = None,
        shipment_date: Optional[date] = None,
        received_date: Optional[date] = None,
        requested_by: int = None,
        approved_by: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.transfer_number = transfer_number
        self.from_warehouse_id = from_warehouse_id
        self.to_warehouse_id = to_warehouse_id
        self.status = status
        self.request_date = request_date or date.today()
        self.approval_date = approval_date
        self.shipment_date = shipment_date
        self.received_date = received_date
        self.requested_by = requested_by
        self.approved_by = approved_by
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transfer_number": self.transfer_number,
            "from_warehouse_id": self.from_warehouse_id,
            "to_warehouse_id": self.to_warehouse_id,
            "status": self.status,
            "request_date": self.request_date,
            "approval_date": self.approval_date,
            "shipment_date": self.shipment_date,
            "received_date": self.received_date,
            "requested_by": self.requested_by,
            "approved_by": self.approved_by,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TransferModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            transfer_number=data.get("transfer_number"),
            from_warehouse_id=data.get("from_warehouse_id"),
            to_warehouse_id=data.get("to_warehouse_id"),
            status=data.get("status", "en_attente"),
            request_date=data.get("request_date"),
            approval_date=data.get("approval_date"),
            shipment_date=data.get("shipment_date"),
            received_date=data.get("received_date"),
            requested_by=data.get("requested_by"),
            approved_by=data.get("approved_by"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "recu"
    
    def is_pending(self) -> bool:
        """Vérifie si en attente"""
        return self.status == "en_attente"


class TransferItemModel:
    """Modèle d'article de transfert"""
    
    def __init__(
        self,
        id: int,
        transfer_id: int,
        product_id: int,
        quantity_requested: float,
        quantity_shipped: float = 0,
        quantity_received: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.transfer_id = transfer_id
        self.product_id = product_id
        self.quantity_requested = quantity_requested
        self.quantity_shipped = quantity_shipped
        self.quantity_received = quantity_received
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transfer_id": self.transfer_id,
            "product_id": self.product_id,
            "quantity_requested": self.quantity_requested,
            "quantity_shipped": self.quantity_shipped,
            "quantity_received": self.quantity_received,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_fully_received(self) -> bool:
        """Vérifie si entièrement reçu"""
        return self.quantity_received >= self.quantity_requested


class TransferApprovalModel:
    """Modèle d'approbation de transfert"""
    
    def __init__(
        self,
        id: int,
        transfer_id: int,
        approved_by: int,
        approval_date: date = None,
        status: str = "approuve",
        comments: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.transfer_id = transfer_id
        self.approved_by = approved_by
        self.approval_date = approval_date or date.today()
        self.status = status
        self.comments = comments
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transfer_id": self.transfer_id,
            "approved_by": self.approved_by,
            "approval_date": self.approval_date,
            "status": self.status,
            "comments": self.comments,
            "created_at": self.created_at
        }
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"
