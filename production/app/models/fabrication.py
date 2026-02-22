"""
Modèle de données pour la fabrication

Ce module définit le modèle de données pour la gestion
de la fabrication dans le module de production.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class ManufacturingOrderModel:
    """Modèle d'ordre de fabrication"""
    
    def __init__(
        self,
        id: int,
        order_number: str,
        product_id: int,
        quantity: float = 1,
        status: str = "planifie",
        priority: str = "normale",
        planned_start: Optional[date] = None,
        planned_end: Optional[date] = None,
        actual_start: Optional[date] = None,
        actual_end: Optional[date] = None,
        bom_id: Optional[int] = None,
        workstation_id: Optional[int] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        approved_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_number = order_number
        self.product_id = product_id
        self.quantity = quantity
        self.status = status
        self.priority = priority
        self.planned_start = planned_start
        self.planned_end = planned_end
        self.actual_start = actual_start
        self.actual_end = actual_end
        self.bom_id = bom_id
        self.workstation_id = workstation_id
        self.notes = notes
        self.created_by = created_by
        self.approved_by = approved_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "status": self.status,
            "priority": self.priority,
            "planned_start": self.planned_start,
            "planned_end": self.planned_end,
            "actual_start": self.actual_start,
            "actual_end": self.actual_end,
            "bom_id": self.bom_id,
            "workstation_id": self.workstation_id,
            "notes": self.notes,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ManufacturingOrderModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            order_number=data.get("order_number"),
            product_id=data.get("product_id"),
            quantity=data.get("quantity", 1),
            status=data.get("status", "planifie"),
            priority=data.get("priority", "normale"),
            planned_start=data.get("planned_start"),
            planned_end=data.get("planned_end"),
            actual_start=data.get("actual_start"),
            actual_end=data.get("actual_end"),
            bom_id=data.get("bom_id"),
            workstation_id=data.get("workstation_id"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            approved_by=data.get("approved_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si l'ordre est terminé"""
        return self.status == "termine"
    
    def is_in_progress(self) -> bool:
        """Vérifie si l'ordre est en cours"""
        return self.status == "en_cours"
    
    def is_delayed(self) -> bool:
        """Vérifie si l'ordre est retardé"""
        if self.is_completed() or not self.planned_end:
            return False
        return date.today() > self.planned_end


class WorkOrderModel:
    """Modèle d'ordre de travail"""
    
    def __init__(
        self,
        id: int,
        manufacturing_order_id: int,
        workstation_id: int,
        operation_sequence: int,
        status: str = "en_attente",
        planned_duration: float = 0,
        actual_duration: float = 0,
        planned_start: Optional[datetime] = None,
        planned_end: Optional[datetime] = None,
        actual_start: Optional[datetime] = None,
        actual_end: Optional[datetime] = None,
        operator_id: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.manufacturing_order_id = manufacturing_order_id
        self.workstation_id = workstation_id
        self.operation_sequence = operation_sequence
        self.status = status
        self.planned_duration = planned_duration
        self.actual_duration = actual_duration
        self.planned_start = planned_start
        self.planned_end = planned_end
        self.actual_start = actual_start
        self.actual_end = actual_end
        self.operator_id = operator_id
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "manufacturing_order_id": self.manufacturing_order_id,
            "workstation_id": self.workstation_id,
            "operation_sequence": self.operation_sequence,
            "status": self.status,
            "planned_duration": self.planned_duration,
            "actual_duration": self.actual_duration,
            "planned_start": self.planned_start,
            "planned_end": self.planned_end,
            "actual_start": self.actual_start,
            "actual_end": self.actual_end,
            "operator_id": self.operator_id,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si le travail est terminé"""
        return self.status == "termine"
    
    def efficiency(self) -> float:
        """Calcule l'efficacité"""
        if self.planned_duration == 0:
            return 0
        return (self.planned_duration / self.actual_duration) * 100 if self.actual_duration > 0 else 0


class QualityControlModel:
    """Modèle de contrôle qualité"""
    
    def __init__(
        self,
        id: int,
        manufacturing_order_id: int,
        inspection_date: Optional[date] = None,
        inspector_id: int = None,
        quantity_checked: float = 0,
        quantity_accepted: float = 0,
        quantity_rejected: float = 0,
        status: str = "en_attente",
        defect_description: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.manufacturing_order_id = manufacturing_order_id
        self.inspection_date = inspection_date
        self.inspector_id = inspector_id
        self.quantity_checked = quantity_checked
        self.quantity_accepted = quantity_accepted
        self.quantity_rejected = quantity_rejected
        self.status = status
        self.defect_description = defect_description
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "manufacturing_order_id": self.manufacturing_order_id,
            "inspection_date": self.inspection_date,
            "inspector_id": self.inspector_id,
            "quantity_checked": self.quantity_checked,
            "quantity_accepted": self.quantity_accepted,
            "quantity_rejected": self.quantity_rejected,
            "status": self.status,
            "defect_description": self.defect_description,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def acceptance_rate(self) -> float:
        """Calcule le taux d'acceptation"""
        if self.quantity_checked == 0:
            return 0
        return (self.quantity_accepted / self.quantity_checked) * 100
    
    def is_passed(self) -> bool:
        """Vérifie si le contrôle est passé"""
        return self.status == "reussi"
