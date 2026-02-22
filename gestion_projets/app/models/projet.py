"""
Modèle de données pour les projets

Ce module définit le modèle de données pour les projets
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class ProjectModel:
    """Modèle de projet"""
    
    def __init__(
        self,
        id: int,
        name: str,
        project_type: str = "interne",
        status: str = "planification",
        priority: str = "moyenne",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        budget: float = 0,
        actual_cost: float = 0,
        description: Optional[str] = None,
        client_id: Optional[int] = None,
        manager_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.project_type = project_type
        self.status = status
        self.priority = priority
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.actual_cost = actual_cost
        self.description = description
        self.client_id = client_id
        self.manager_id = manager_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "project_type": self.project_type,
            "status": self.status,
            "priority": self.priority,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "actual_cost": self.actual_cost,
            "description": self.description,
            "client_id": self.client_id,
            "manager_id": self.manager_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            project_type=data.get("project_type", "interne"),
            status=data.get("status", "planification"),
            priority=data.get("priority", "moyenne"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            budget=data.get("budget", 0),
            actual_cost=data.get("actual_cost", 0),
            description=data.get("description"),
            client_id=data.get("client_id"),
            manager_id=data.get("manager_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si le projet est actif"""
        return self.status in ["en_cours", "planification"]
    
    def is_overdue(self) -> bool:
        """Vérifie si le projet est en retard"""
        if not self.end_date:
            return False
        return date.today() > self.end_date and self.status != "termine"
    
    def budget_usage_percent(self) -> float:
        """Calcule le pourcentage d'utilisation du budget"""
        if self.budget == 0:
            return 0
        return (self.actual_cost / self.budget) * 100


class TaskModel:
    """Modèle de tâche"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        description: Optional[str] = None,
        status: str = "a_faire",
        priority: str = "moyenne",
        start_date: Optional[date] = None,
        due_date: Optional[date] = None,
        estimated_hours: float = 0,
        actual_hours: float = 0,
        progress: int = 0,
        assignee_id: Optional[int] = None,
        parent_task_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.status = status
        self.priority = priority
        self.start_date = start_date
        self.due_date = due_date
        self.estimated_hours = estimated_hours
        self.actual_hours = actual_hours
        self.progress = progress
        self.assignee_id = assignee_id
        self.parent_task_id = parent_task_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "progress": self.progress,
            "assignee_id": self.assignee_id,
            "parent_task_id": self.parent_task_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si la tâche est terminée"""
        return self.status == "terminee"
    
    def is_overdue(self) -> bool:
        """Vérifie si la tâche est en retard"""
        if not self.due_date or self.is_completed():
            return False
        return date.today() > self.due_date
    
    def update_progress(self):
        """Met à jour la progression basée sur le temps"""
        if self.estimated_hours > 0:
            self.progress = min(100, int((self.actual_hours / self.estimated_hours) * 100))


class MilestoneModel:
    """Modèle de jalon"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        description: Optional[str] = None,
        due_date: Optional[date] = None,
        status: str = "en_attente",
        is_completed: bool = False,
        completed_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.status = status
        self.is_completed = is_completed
        self.completed_at = completed_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "is_completed": self.is_completed,
            "completed_at": self.completed_at,
            "created_at": self.created_at
        }
    
    def complete(self):
        """Marque le jalon comme terminé"""
        self.is_completed = True
        self.status = "termine"
        self.completed_at = datetime.now()


class ProjectTeamModel:
    """Modèle d'équipe de projet"""
    
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
    
    def is_manager(self) -> bool:
        """Vérifie si l'utilisateur est gestionnaire"""
        return self.role == "gestionnaire"
