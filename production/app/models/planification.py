"""
Modèle de données pour la planification de production

Ce module définit le modèle de données pour la planification
dans le module de production.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class MasterScheduleModel:
    """Modèle de programme directeur de production"""
    
    def __init__(
        self,
        id: int,
        schedule_number: str,
        period_start: date,
        period_end: date,
        status: str = "brouillon",
        total_planned: float = 0,
        total_completed: float = 0,
        notes: Optional[str] = None,
        created_by: int = None,
        approved_by: Optional[int] = None,
        approved_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.schedule_number = schedule_number
        self.period_start = period_start
        self.period_end = period_end
        self.status = status
        self.total_planned = total_planned
        self.total_completed = total_completed
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
            "schedule_number": self.schedule_number,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "status": self.status,
            "total_planned": self.total_planned,
            "total_completed": self.total_completed,
            "notes": self.notes,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MasterScheduleModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            schedule_number=data.get("schedule_number"),
            period_start=data.get("period_start"),
            period_end=data.get("period_end"),
            status=data.get("status", "brouillon"),
            total_planned=data.get("total_planned", 0),
            total_completed=data.get("total_completed", 0),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            approved_by=data.get("approved_by"),
            approved_at=data.get("approved_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def completion_rate(self) -> float:
        """Calcule le taux d'achèvement"""
        if self.total_planned == 0:
            return 0
        return (self.total_completed / self.total_planned) * 100
    
    def is_completed(self) -> bool:
        """Vérifie si le programme est terminé"""
        return self.status == "termine"


class ScheduleLineModel:
    """Modèle de ligne de programme"""
    
    def __init__(
        self,
        id: int,
        schedule_id: int,
        product_id: int,
        quantity: float = 0,
        date: Optional[date] = None,
        priority: str = "normale",
        status: str = "planifie",
        produced_quantity: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.schedule_id = schedule_id
        self.product_id = product_id
        self.quantity = quantity
        self.date = date
        self.priority = priority
        self.status = status
        self.produced_quantity = produced_quantity
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "schedule_id": self.schedule_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "date": self.date,
            "priority": self.priority,
            "status": self.status,
            "produced_quantity": self.produced_quantity,
            "created_at": self.created_at
        }
    
    def completion_percentage(self) -> float:
        """Calcule le pourcentage d'achèvement"""
        if self.quantity == 0:
            return 0
        return (self.produced_quantity / self.quantity) * 100


class CapacityPlanningModel:
    """Modèle de planification de capacité"""
    
    def __init__(
        self,
        id: int,
        workstation_id: int,
        date: date,
        available_capacity: float = 0,
        allocated_capacity: float = 0,
        efficiency_rate: float = 100,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.workstation_id = workstation_id
        self.date = date
        self.available_capacity = available_capacity
        self.allocated_capacity = allocated_capacity
        self.efficiency_rate = efficiency_rate
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "workstation_id": self.workstation_id,
            "date": self.date,
            "available_capacity": self.available_capacity,
            "allocated_capacity": self.allocated_capacity,
            "efficiency_rate": self.efficiency_rate,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def utilization_rate(self) -> float:
        """Calcule le taux d'utilisation"""
        if self.available_capacity == 0:
            return 0
        return (self.allocated_capacity / self.available_capacity) * 100
    
    def available_time(self) -> float:
        """Calcule le temps disponible"""
        return self.available_capacity - self.allocated_capacity
