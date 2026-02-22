"""
Modèle de données pour les projets

Ce module définit le modèle de données pour les projets
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class ProjectModel:
    """Modèle de projet"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        client_id: Optional[int] = None,
        manager_id: int = None,
        status: str = "planifie",
        budget: Optional[float] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        completion_percent: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.client_id = client_id
        self.manager_id = manager_id
        self.status = status
        self.budget = budget
        self.start_date = start_date
        self.end_date = end_date
        self.completion_percent = completion_percent
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "client_id": self.client_id,
            "manager_id": self.manager_id,
            "status": self.status,
            "budget": self.budget,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "completion_percent": self.completion_percent,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            description=data.get("description"),
            client_id=data.get("client_id"),
            manager_id=data.get("manager_id"),
            status=data.get("status", "planifie"),
            budget=data.get("budget"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            completion_percent=data.get("completion_percent", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si le projet est actif"""
        return self.status in ["planifie", "en_cours"]
    
    def is_completed(self) -> bool:
        """Vérifie si le projet est terminé"""
        return self.status == "termine" or self.completion_percent == 100


class ProjectMemberModel:
    """Modèle de membre de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        user_id: int,
        role: str = "membre",
        joined_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.role = role
        self.joined_at = joined_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "role": self.role,
            "joined_at": self.joined_at
        }


class MilestoneModel:
    """Modèle de jalon"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        is_completed: bool = False,
        completed_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.is_completed = is_completed
        self.completed_at = completed_at
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
            "is_completed": self.is_completed,
            "completed_at": self.completed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def mark_completed(self):
        """Marque le jalon comme terminé"""
        self.is_completed = True
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """Vérifie si le jalon est en retard"""
        if self.due_date and not self.is_completed:
            return datetime.now() > self.due_date
        return False
