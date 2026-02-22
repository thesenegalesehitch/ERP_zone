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
        movement_type: str,
        quantity: float = 0,
        unit_cost: float = 0,
        total_cost: float = 0,
        reference: Optional[str] = None,
        movement_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.movement_type = movement_type
        self.quantity = quantity
        self.unit_cost = unit_cost
        self.total_cost = total_cost
        self.reference = reference
        self.movement_date = movement_date
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "unit_cost": self.unit_cost,
            "total_cost": self.total_cost,
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
            movement_type=data.get("movement_type"),
            quantity=data.get("quantity", 0),
            unit_cost=data.get("unit_cost", 0),
            total_cost=data.get("total_cost", 0),
            reference=data.get("reference"),
            movement_date=data.get("movement_date"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at")
        )
    
    def calculate_total(self):
        """Calcule le coût total"""
        self.total_cost = self.quantity * self.unit_cost
    
    def is_inflow(self) -> bool:
        """Vérifie si c'est une entrée"""
        return self.movement_type in ["entree", "achat", "retour", "ajustement_positif"]
    
    def is_outflow(self) -> bool:
        """Vérifie si c'est une sortie"""
        return self.movement_type in ["sortie", "vente", "perte", "ajustement_negatif"]


class StockAdjustmentModel:
    """Modèle d'ajustement de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        adjustment_type: str,
        quantity_before: float = 0,
        quantity_after: float = 0,
        difference: float = 0,
        reason: Optional[str] = None,
        reference: Optional[str] = None,
        adjustment_date: Optional[date] = None,
        status: str = "en_attente",
        approved_by: Optional[int] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.adjustment_type = adjustment_type
        self.quantity_before = quantity_before
        self.quantity_after = quantity_after
        self.difference = difference
        self.reason = reason
        self.reference = reference
        self.adjustment_date = adjustment_date
        self.status = status
        self.approved_by = approved_by
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "adjustment_type": self.adjustment_type,
            "quantity_before": self.quantity_before,
            "quantity_after": self.quantity_after,
            "difference": self.difference,
            "reason": self.reason,
            "reference": self.reference,
            "adjustment_date": self.adjustment_date,
            "status": self.status,
            "approved_by": self.approved_by,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_difference(self):
        """Calcule la différence"""
        self.difference = self.quantity_after - self.quantity_before
    
    def is_increase(self) -> bool:
        """Vérifie si c'est une augmentation"""
        return self.difference > 0
    
    def is_approved(self) -> bool:
        """Vérifie si l'ajustement est approuvé"""
        return self.status == "approuve"


class StockCountModel:
    """Modèle d'inventaire"""
    
    def __init__(
        self,
        id: int,
        count_number: str,
        warehouse_id: int,
        count_date: Optional[date] = None,
        status: str = "en_cours",
        total_products: int = 0,
        counted_products: int = 0,
        discrepancies: int = 0,
        notes: Optional[str] = None,
        started_by: int = None,
        completed_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.count_number = count_number
        self.warehouse_id = warehouse_id
        self.count_date = count_date
        self.status = status
        self.total_products = total_products
        self.counted_products = counted_products
        self.discrepancies = discrepancies
        self.notes = notes
        self.started_by = started_by
        self.completed_by = completed_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "count_number": self.count_number,
            "warehouse_id": self.warehouse_id,
            "count_date": self.count_date,
            "status": self.status,
            "total_products": self.total_products,
            "counted_products": self.counted_products,
            "discrepancies": self.discrepancies,
            "notes": self.notes,
            "started_by": self.started_by,
            "completed_by": self.completed_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def completion_percentage(self) -> float:
        """Calcule le pourcentage d'achèvement"""
        if self.total_products == 0:
            return 0
        return (self.counted_products / self.total_products) * 100
    
    def is_completed(self) -> bool:
        """Vérifie si l'inventaire est terminé"""
        return self.status == "termine"
