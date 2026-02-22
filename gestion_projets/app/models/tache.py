"""
Modèle de données pour les tâches

Ce module définit le modèle de données pour les tâches
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class TaskModel:
    """Modèle de tâche"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        task_type: str = "generale",
        priority: str = "moyenne",
        status: str = "a_faire",
        assignee_id: Optional[int] = None,
        start_date: Optional[date] = None,
        due_date: Optional[date] = None,
        completed_date: Optional[date] = None,
        estimated_hours: float = 0,
        actual_hours: float = 0,
        progress: float = 0,
        parent_id: Optional[int] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.task_type = task_type
        self.priority = priority
        self.status = status
        self.assignee_id = assignee_id
        self.start_date = start_date
        self.due_date = due_date
        self.completed_date = completed_date
        self.estimated_hours = estimated_hours
        self.actual_hours = actual_hours
        self.progress = progress
        self.parent_id = parent_id
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "task_type": self.task_type,
            "priority": self.priority,
            "status": self.status,
            "assignee_id": self.assignee_id,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "completed_date": self.completed_date,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "progress": self.progress,
            "parent_id": self.parent_id,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TaskModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            title=data.get("title"),
            description=data.get("description"),
            task_type=data.get("task_type", "generale"),
            priority=data.get("priority", "moyenne"),
            status=data.get("status", "a_faire"),
            assignee_id=data.get("assignee_id"),
            start_date=data.get("start_date"),
            due_date=data.get("due_date"),
            completed_date=data.get("completed_date"),
            estimated_hours=data.get("estimated_hours", 0),
            actual_hours=data.get("actual_hours", 0),
            progress=data.get("progress", 0),
            parent_id=data.get("parent_id"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si terminée"""
        return self.status == "terminee"
    
    def is_overdue(self) -> bool:
        """Vérifie si en retard"""
        if not self.due_date or self.is_completed():
            return False
        return date.today() > self.due_date
    
    def is_delayed(self) -> bool:
        """Vérifie si retardée"""
        if self.estimated_hours == 0:
            return False
        return self.actual_hours > self.estimated_hours


class SubTaskModel:
    """Modèle de sous-tâche"""
    
    def __init__(
        self,
        id: int,
        task_id: int,
        title: str,
        status: str = "a_faire",
        completed: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.task_id = task_id
        self.title = title
        self.status = status
        self.completed = completed
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "title": self.title,
            "status": self.status,
            "completed": self.completed,
            "created_at": self.created_at
        }


class TaskCommentModel:
    """Modèle de commentaire de tâche"""
    
    def __init__(
        self,
        id: int,
        task_id: int,
        user_id: int,
        content: str,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.task_id = task_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at
        }
