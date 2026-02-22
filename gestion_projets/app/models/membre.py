"""
Modèle de données pour les membres d'équipe

Ce module définit le modèle de données pour les membres d'équipe
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class ProjectMemberModel:
    """Modèle de membre de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        user_id: int,
        role: str = "membre",
        allocation_percentage: float = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.role = role
        self.allocation_percentage = allocation_percentage
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "role": self.role,
            "allocation_percentage": self.allocation_percentage,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectMemberModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            user_id=data.get("user_id"),
            role=data.get("role", "membre"),
            allocation_percentage=data.get("allocation_percentage", 100),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at")
        )
    
    def is_project_manager(self) -> bool:
        """Vérifie si gestionnaire de projet"""
        return self.role == "gestionnaire"
    
    def is_fully_allocated(self) -> bool:
        """Vérifie si entièrement alloué"""
        return self.allocation_percentage >= 100


class MemberAssignmentModel:
    """Modèle d'affectation de membre"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        task_id: int,
        assigned_date: date = None,
        status: str = "active",
        allocated_hours: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.task_id = task_id
        self.assigned_date = assigned_date
        self.status = status
        self.allocated_hours = allocated_hours
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "task_id": self.task_id,
            "assigned_date": self.assigned_date,
            "status": self.status,
            "allocated_hours": self.allocated_hours,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_active_assignment(self) -> bool:
        """Vérifie si affectation active"""
        return self.status == "active"


class MemberWorkloadModel:
    """Modèle de charge de travail"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        date: date = None,
        planned_hours: float = 0,
        actual_hours: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.date = date
        self.planned_hours = planned_hours
        self.actual_hours = actual_hours
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "date": self.date,
            "planned_hours": self.planned_hours,
            "actual_hours": self.actual_hours,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def utilization_percentage(self) -> float:
        """Pourcentage d'utilisation"""
        if self.planned_hours == 0:
            return 0
        return (self.actual_hours / self.planned_hours) * 100
