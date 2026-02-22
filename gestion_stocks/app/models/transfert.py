"""
Modèle de données pour les transferts

Ce module définit le modèle de données pour les transferts
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class StockTransferModel:
    """Modèle de transfert de stock"""
    
    def __init__(
        self,
        id: int,
        transfer_number: str,
        from_warehouse_id: int,
        to_warehouse_id: int,
        transfer_date: date = None,
        status: str = "en_attente",
        notes: Optional[str] = None,
        created_by: int = None,
        approved_by: Optional[int] = None,
        received_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.transfer_number = transfer_number
        self.from_warehouse_id = from_warehouse_id
        self.to_warehouse_id = to_warehouse_id
        self.transfer_date = transfer_date
        self.status = status
        self.notes = notes
        self.created_by = created_by
        self.approved_by = approved_by
        self.received_by = received_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transfer_number": self.transfer_number,
            "from_warehouse_id": self.from_warehouse_id,
            "to_warehouse_id": self.to_warehouse_id,
            "transfer_date": self.transfer_date,
            "status": self.status,
            "notes": self.notes,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "received_by": self.received_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StockTransferModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            transfer_number=data.get("transfer_number"),
            from_warehouse_id=data.get("from_warehouse_id"),
            to_warehouse_id=data.get("to_warehouse_id"),
            transfer_date=data.get("transfer_date"),
            status=data.get("status", "en_attente"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            approved_by=data.get("approved_by"),
            received_by=data.get("received_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"
    
    def is_received(self) -> bool:
        """Vérifie si reçu"""
        return self.status == "recus"


class TransferLineModel:
    """Modèle de ligne de transfert"""
    
    def __init__(
        self,
        id: int,
        transfer_id: int,
        product_id: int,
        quantity: float = 0,
        sent_quantity: float = 0,
        received_quantity: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.transfer_id = transfer_id
        self.product_id = product_id
        self.quantity = quantity
        self.sent_quantity = sent_quantity
        self.received_quantity = received_quantity
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transfer_id": self.transfer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "sent_quantity": self.sent_quantity,
            "received_quantity": self.received_quantity,
            "created_at": self.created_at
        }
    
    def is_fully_sent(self) -> bool:
        """Vérifie si entièrement envoyé"""
        return self.sent_quantity >= self.quantity
    
    def is_fully_received(self) -> bool:
        """Vérifie si entièrement reçu"""
        return self.received_quantity >= self.sent_quantity


class StockReservationModel:
    """Modèle de réservation de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        warehouse_id: int,
        quantity: float = 0,
        reserved_for: Optional[str] = None,
        reference: Optional[str] = None,
        status: str = "actif",
        expiry_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.quantity = quantity
        self.reserved_for = reserved_for
        self.reference = reference
        self.status = status
        self.expiry_date = expiry_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "quantity": self.quantity,
            "reserved_for": self.reserved_for,
            "reference": self.reference,
            "status": self.status,
            "expiry_date": self.expiry_date,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_expired(self) -> bool:
        """Vérifie si expiré"""
        if not self.expiry_date:
            return False
        return date.today() > self.expiry_date
