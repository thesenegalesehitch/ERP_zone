"""
Modèle de données pour les interactions clients

Ce module définit le modèle de données pour les interactions
dans le module de gestion des clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class InteractionModel:
    """Modèle d'interaction"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        interaction_type: str,
        subject: str,
        description: Optional[str] = None,
        direction: str = "entrante",
        status: str = "planifiee",
        priority: str = "normale",
        assigned_to: Optional[int] = None,
        scheduled_date: Optional[datetime] = None,
        completed_date: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.interaction_type = interaction_type
        self.subject = subject
        self.description = description
        self.direction = direction
        self.status = status
        self.priority = priority
        self.assigned_to = assigned_to
        self.scheduled_date = scheduled_date
        self.completed_date = completed_date
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "interaction_type": self.interaction_type,
            "subject": self.subject,
            "description": self.description,
            "direction": self.direction,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "scheduled_date": self.scheduled_date,
            "completed_date": self.completed_date,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "InteractionModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            client_id=data.get("client_id"),
            interaction_type=data.get("interaction_type"),
            subject=data.get("subject"),
            description=data.get("description"),
            direction=data.get("direction", "entrante"),
            status=data.get("status", "planifiee"),
            priority=data.get("priority", "normale"),
            assigned_to=data.get("assigned_to"),
            scheduled_date=data.get("scheduled_date"),
            completed_date=data.get("completed_date"),
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
        if not self.scheduled_date or self.is_completed():
            return False
        return datetime.now() > self.scheduled_date


class InteractionNoteModel:
    """Modèle de note d'interaction"""
    
    def __init__(
        self,
        id: int,
        interaction_id: int,
        content: str,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.interaction_id = interaction_id
        self.content = content
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "interaction_id": self.interaction_id,
            "content": self.content,
            "created_by": self.created_by,
            "created_at": self.created_at
        }


class InteractionAttachmentModel:
    """Modèle de pièce jointe d'interaction"""
    
    def __init__(
        self,
        id: int,
        interaction_id: int,
        file_name: str,
        file_path: str,
        file_type: Optional[str] = None,
        file_size: Optional[int] = None,
        uploaded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.interaction_id = interaction_id
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_type
        self.file_size = file_size
        self.uploaded_by = uploaded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "interaction_id": self.interaction_id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at
        }
