"""
Modèle de données pour la capacité de production

Ce module définit le modèle de données pour la capacité
dans le module de production.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class WorkstationModel:
    """Modèle de poste de travail"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        workstation_type: str = "standard",
        capacity: float = 8,
        efficiency_rate: float = 100,
        status: str = "disponible",
        location: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.workstation_type = workstation_type
        self.capacity = capacity
        self.efficiency_rate = efficiency_rate
        self.status = status
        self.location = location
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "workstation_type": self.workstation_type,
            "capacity": self.capacity,
            "efficiency_rate": self.efficiency_rate,
            "status": self.status,
            "location": self.location,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "WorkstationModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            code=data.get("code"),
            workstation_type=data.get("workstation_type", "standard"),
            capacity=data.get("capacity", 8),
            efficiency_rate=data.get("efficiency_rate", 100),
            status=data.get("status", "disponible"),
            location=data.get("location"),
            description=data.get("description"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_available(self) -> bool:
        """Vérifie si disponible"""
        return self.status == "disponible"
    
    def effective_capacity(self) -> float:
        """Capacité effective"""
        return self.capacity * (self.efficiency_rate / 100)


class WorkcenterModel:
    """Modèle de centre de travail"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        workstation_ids: Optional[str] = None,
        capacity: float = 0,
        efficiency_rate: float = 100,
        status: str = "actif",
        manager_id: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.workstation_ids = workstation_ids
        self.capacity = capacity
        self.efficiency_rate = efficiency_rate
        self.status = status
        self.manager_id = manager_id
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "workstation_ids": self.workstation_ids,
            "capacity": self.capacity,
            "efficiency_rate": self.efficiency_rate,
            "status": self.status,
            "manager_id": self.manager_id,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"
    
    def get_workstation_list(self) -> list:
        """Liste des postes de travail"""
        if not self.workstation_ids:
            return []
        return [int(x.strip()) for x in self.workstation_ids.split(",")]


class DowntimeModel:
    """Modèle d'indisponibilité"""
    
    def __init__(
        self,
        id: int,
        workstation_id: int,
        downtime_type: str,
        start_date: datetime = None,
        end_date: Optional[datetime] = None,
        duration_hours: float = 0,
        reason: Optional[str] = None,
        status: str = "en_cours",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.workstation_id = workstation_id
        self.downtime_type = downtime_type
        self.start_date = start_date
        self.end_date = end_date
        self.duration_hours = duration_hours
        self.reason = reason
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "workstation_id": self.workstation_id,
            "downtime_type": self.downtime_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "duration_hours": self.duration_hours,
            "reason": self.reason,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_duration(self):
        """Calcule la durée"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.duration_hours = delta.total_seconds() / 3600
    
    def is_active(self) -> bool:
        """Vérifie si active"""
        return self.status == "en_cours"
