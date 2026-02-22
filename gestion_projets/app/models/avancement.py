"""
Modèle de données pour le suivi d'avancement

Ce module définit le modèle de données pour le suivi d'avancement
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class ProgressTrackingModel:
    """Modèle de suivi d'avancement"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        task_id: int,
        progress_percentage: float = 0,
        status: str = "en_cours",
        notes: Optional[str] = None,
        updated_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.task_id = task_id
        self.progress_percentage = progress_percentage
        self.status = status
        self.notes = notes
        self.updated_by = updated_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "task_id": self.task_id,
            "progress_percentage": self.progress_percentage,
            "status": self.status,
            "notes": self.notes,
            "updated_by": self.updated_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProgressTrackingModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            task_id=data.get("task_id"),
            progress_percentage=data.get("progress_percentage", 0),
            status=data.get("status", "en_cours"),
            notes=data.get("notes"),
            updated_by=data.get("updated_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.progress_percentage >= 100


class ProgressUpdateModel:
    """Modèle de mise à jour d'avancement"""
    
    def __init__(
        self,
        id: int,
        tracking_id: int,
        previous_percentage: float,
        new_percentage: float,
        update_date: date = None,
        notes: Optional[str] = None,
        updated_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.tracking_id = tracking_id
        self.previous_percentage = previous_percentage
        self.new_percentage = new_percentage
        self.update_date = update_date or date.today()
        self.notes = notes
        self.updated_by = updated_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "tracking_id": self.tracking_id,
            "previous_percentage": self.previous_percentage,
            "new_percentage": self.new_percentage,
            "update_date": self.update_date,
            "notes": self.notes,
            "updated_by": self.updated_by,
            "created_at": self.created_at
        }
    
    def change_percentage(self) -> float:
        """Pourcentage de changement"""
        return self.new_percentage - self.previous_percentage


class ProjectSummaryModel:
    """Modèle de résumé de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        total_tasks: int = 0,
        completed_tasks: int = 0,
        in_progress_tasks: int = 0,
        pending_tasks: int = 0,
        overall_progress: float = 0,
        summary_date: date = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.total_tasks = total_tasks
        self.completed_tasks = completed_tasks
        self.in_progress_tasks = in_progress_tasks
        self.pending_tasks = pending_tasks
        self.overall_progress = overall_progress
        self.summary_date = summary_date or date.today()
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "in_progress_tasks": self.in_progress_tasks,
            "pending_tasks": self.pending_tasks,
            "overall_progress": self.overall_progress,
            "summary_date": self.summary_date,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def completion_rate(self) -> float:
        """Taux de complétion"""
        if self.total_tasks == 0:
            return 0
        return (self.completed_tasks / self.total_tasks) * 100
