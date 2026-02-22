"""
Modèle de données pour les membres de projet

Ce module définit le modèle de données pour les membres
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class MemberModel:
    """Modèle de membre"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        user_id: int,
        role: str = "membre",
        joined_date: date = None,
        is_active: bool = True,
        allocated_hours: float = 0,
        hourly_rate: float = 0,
        notes: Optional[str] = None,
        added_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.role = role
        self.joined_date = joined_date or date.today()
        self.is_active = is_active
        self.allocated_hours = allocated_hours
        self.hourly_rate = hourly_rate
        self.notes = notes
        self.added_by = added_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "role": self.role,
            "joined_date": self.joined_date,
            "is_active": self.is_active,
            "allocated_hours": self.allocated_hours,
            "hourly_rate": self.hourly_rate,
            "notes": self.notes,
            "added_by": self.added_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MemberModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            user_id=data.get("user_id"),
            role=data.get("role", "membre"),
            joined_date=data.get("joined_date"),
            is_active=data.get("is_active", True),
            allocated_hours=data.get("allocated_hours", 0),
            hourly_rate=data.get("hourly_rate", 0),
            notes=data.get("notes"),
            added_by=data.get("added_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active_member(self) -> bool:
        """Vérifie si actif"""
        return self.is_active
    
    def total_cost(self) -> float:
        """Coût total"""
        return self.allocated_hours * self.hourly_rate


class MemberAssignmentModel:
    """Modèle d'affectation de membre"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        task_id: int,
        allocated_hours: float = 0,
        start_date: date = None,
        end_date: Optional[date] = None,
        status: str = "actif",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.task_id = task_id
        self.allocated_hours = allocated_hours
        self.start_date = start_date or date.today()
        self.end_date = end_date
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "task_id": self.task_id,
            "allocated_hours": self.allocated_hours,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_active_assignment(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"


class MemberAvailabilityModel:
    """Modèle de disponibilité de membre"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        date: date,
        available_hours: float = 8,
        is_available: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.date = date
        self.available_hours = available_hours
        self.is_available = is_available
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "date": self.date,
            "available_hours": self.available_hours,
            "is_available": self.is_available,
            "notes": self.notes,
            "created_at": self.created_at
        }
