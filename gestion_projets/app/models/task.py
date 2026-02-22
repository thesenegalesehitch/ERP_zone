"""
Modèle de données pour les tâches

Ce module définit le modèle de données pour les tâches
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class TaskModel:
    """Modèle de tâche"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        assignee_id: Optional[int] = None,
        status: str = "a_faire",
        priority: str = "moyenne",
        estimated_hours: Optional[float] = None,
        actual_hours: Optional[float] = None,
        start_date: Optional[datetime] = None,
        due_date: Optional[datetime] = None,
        completion_date: Optional[datetime] = None,
        parent_task_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.assignee_id = assignee_id
        self.status = status
        self.priority = priority
        self.estimated_hours = estimated_hours
        self.actual_hours = actual_hours
        self.start_date = start_date
        self.due_date = due_date
        self.completion_date = completion_date
        self.parent_task_id = parent_task_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "assignee_id": self.assignee_id,
            "status": self.status,
            "priority": self.priority,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "completion_date": self.completion_date,
            "parent_task_id": self.parent_task_id,
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
            assignee_id=data.get("assignee_id"),
            status=data.get("status", "a_faire"),
            priority=data.get("priority", "moyenne"),
            estimated_hours=data.get("estimated_hours"),
            actual_hours=data.get("actual_hours"),
            start_date=data.get("start_date"),
            due_date=data.get("due_date"),
            completion_date=data.get("completion_date"),
            parent_task_id=data.get("parent_task_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si la tâche est terminée"""
        return self.status == "terminee"
    
    def is_overdue(self) -> bool:
        """Vérifie si la tâche est en retard"""
        if self.due_date and self.status != "terminee":
            return datetime.now() > self.due_date
        return False
    
    def progress_percent(self) -> int:
        """Calcule le pourcentage de progression"""
        if self.status == "terminee":
            return 100
        elif self.status == "en_cours":
            return 50
        elif self.status == "a_faire":
            return 0
        return 0


class SubTaskModel(TaskModel):
    """Modèle de sous-tâche"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_task_id = kwargs.get("parent_task_id")


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


class TaskAttachmentModel:
    """Modèle de pièce jointe de tâche"""
    
    def __init__(
        self,
        id: int,
        task_id: int,
        filename: str,
        file_path: str,
        file_size: int,
        uploaded_by: int,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.task_id = task_id
        self.filename = filename
        self.file_path = file_path
        self.file_size = file_size
        self.uploaded_by = uploaded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "filename": self.filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at
        }
