"""
Modèle de données pour l'avancement du projet

Ce module définit le modèle de données pour l'avancement
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class MilestoneModel:
    """Modèle d'étape"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        description: Optional[str] = None,
        due_date: date = None,
        completed_date: Optional[date] = None,
        status: str = "en_attente",
        progress: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.completed_date = completed_date
        self.status = status
        self.progress = progress
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date,
            "completed_date": self.completed_date,
            "status": self.status,
            "progress": self.progress,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MilestoneModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            name=data.get("name"),
            description=data.get("description"),
            due_date=data.get("due_date"),
            completed_date=data.get("completed_date"),
            status=data.get("status", "en_attente"),
            progress=data.get("progress", 0),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "termine"
    
    def is_overdue(self) -> bool:
        """Vérifie si en retard"""
        if not self.due_date or self.is_completed():
            return False
        return date.today() > self.due_date


class ProgressUpdateModel:
    """Modèle de mise à jour d'avancement"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        update_date: date = None,
        progress_percentage: float = 0,
        status: str = "en_cours",
        achievements: Optional[str] = None,
        challenges: Optional[str] = None,
        next_steps: Optional[str] = None,
        updated_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.update_date = update_date
        self.progress_percentage = progress_percentage
        self.status = status
        self.achievements = achievements
        self.challenges = challenges
        self.next_steps = next_steps
        self.updated_by = updated_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "update_date": self.update_date,
            "progress_percentage": self.progress_percentage,
            "status": self.status,
            "achievements": self.achievements,
            "challenges": self.challenges,
            "next_steps": self.next_steps,
            "updated_by": self.updated_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class ProjectTimelineModel:
    """Modèle de chronologie de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        phase_name: str,
        start_date: date = None,
        end_date: date = None,
        status: str = "planifie",
        completion_percentage: float = 0,
        dependencies: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.phase_name = phase_name
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.completion_percentage = completion_percentage
        self.dependencies = dependencies
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "phase_name": self.phase_name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "completion_percentage": self.completion_percentage,
            "dependencies": self.dependencies,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def duration_days(self) -> int:
        """Durée en jours"""
        if not self.start_date or not self.end_date:
            return 0
        return (self.end_date - self.start_date).days
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.completion_percentage >= 100
