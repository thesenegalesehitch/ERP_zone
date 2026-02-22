"""
Modèle de données pour les mouvements de stock

Ce module définit le modèle de données pour les mouvements
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class StockMovementModel:
    """Modèle de mouvement de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        warehouse_id: int,
        movement_type: str,
        quantity: float = 0,
        reference: Optional[str] = None,
        movement_date: date = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.movement_type = movement_type
        self.quantity = quantity
        self.reference = reference
        self.movement_date = movement_date or date.today()
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "reference": self.reference,
            "movement_date": self.movement_date,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StockMovementModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            product_id=data.get("product_id"),
            warehouse_id=data.get("warehouse_id"),
            movement_type=data.get("movement_type"),
            quantity=data.get("quantity", 0),
            reference=data.get("reference"),
            movement_date=data.get("movement_date"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at")
        )
    
    def is_entry(self) -> bool:
        """Vérifie si entrée"""
        return self.movement_type in ["entree", "achat", "retour"]
    
    def is_exit(self) -> bool:
        """Vérifie si sortie"""
        return self.movement_type in ["sortie", "vente", "utilisation"]


class StockAdjustmentModel:
    """Modèle d'ajustement de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        warehouse_id: int,
        adjustment_type: str,
        quantity_before: float,
        quantity_after: float,
        reason: str,
        adjustment_date: date = None,
        approved_by: Optional[int] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.adjustment_type = adjustment_type
        self.quantity_before = quantity_before
        self.quantity_after = quantity_after
        self.reason = reason
        self.adjustment_date = adjustment_date or date.today()
        self.approved_by = approved_by
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "adjustment_type": self.adjustment_type,
            "quantity_before": self.quantity_before,
            "quantity_after": self.quantity_after,
            "reason": self.reason,
            "adjustment_date": self.adjustment_date,
            "approved_by": self.approved_by,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at
        }
    
    def difference(self) -> float:
        """Différence de quantité"""
        return self.quantity_after - self.quantity_before


class StockCountModel:
    """Modèle d'inventaire"""
    
    def __init__(
        self,
        id: int,
        warehouse_id: int,
        count_date: date = None,
        status: str = "en_cours",
        counted_by: Optional[int] = None,
        verified_by: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None
    ):
        self.id = id
        self.warehouse_id = warehouse_id
        self.count_date = count_date or date.today()
        self.status = status
        self.counted_by = counted_by
        self.verified_by = verified_by
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.completed_at = completed_at
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "warehouse_id": self.warehouse_id,
            "count_date": self.count_date,
            "status": self.status,
            "counted_by": self.counted_by,
            "verified_by": self.verified_by,
            "notes": self.notes,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "termine"
