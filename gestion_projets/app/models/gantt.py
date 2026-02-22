"""
Modèle de données pour le diagramme de Gantt

Ce module définit le modèle de données pour la planification
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class GanttChartModel:
    """Modèle de diagramme de Gantt"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        start_date: date,
        end_date: date,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "GanttChartModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            title=data.get("title"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def duration_days(self) -> int:
        """Durée en jours"""
        delta = self.end_date - self.start_date
        return delta.days


class GanttTaskModel:
    """Modèle de tâche Gantt"""
    
    def __init__(
        self,
        id: int,
        gantt_chart_id: int,
        task_id: int,
        row: int = 0,
        color: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.gantt_chart_id = gantt_chart_id
        self.task_id = task_id
        self.row = row
        self.color = color
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "gantt_chart_id": self.gantt_chart_id,
            "task_id": self.task_id,
            "row": self.row,
            "color": self.color,
            "created_at": self.created_at
        }


class MilestoneModel:
    """Modèle de jalon"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        description: Optional[str] = None,
        due_date: date = None,
        status: str = "en_attente",
        is_completed: bool = False,
        completed_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.status = status
        self.is_completed = is_completed
        self.completed_date = completed_date
        self.notes = notes
        self.created_by = created_by
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
            "status": self.status,
            "is_completed": self.is_completed,
            "completed_date": self.completed_date,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_completed_status(self) -> bool:
        """Vérifie si terminé"""
        return self.is_completed
