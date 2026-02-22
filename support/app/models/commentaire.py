"""
Modèle de données pour les commentaires

Ce module définit le modèle de données pour les commentaires
dans le module de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class CommentModel:
    """Modèle de commentaire"""
    
    def __init__(
        self,
        id: int,
        ticket_id: int,
        user_id: int,
        content: str,
        is_internal: bool = False,
        is_solution: bool = False,
        parent_id: Optional[int] = None,
        status: str = "nouveau",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.content = content
        self.is_internal = is_internal
        self.is_solution = is_solution
        self.parent_id = parent_id
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "content": self.content,
            "is_internal": self.is_internal,
            "is_solution": self.is_solution,
            "parent_id": self.parent_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CommentModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            ticket_id=data.get("ticket_id"),
            user_id=data.get("user_id"),
            content=data.get("content"),
            is_internal=data.get("is_internal", False),
            is_solution=data.get("is_solution", False),
            parent_id=data.get("parent_id"),
            status=data.get("status", "nouveau"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_edited(self) -> bool:
        """Vérifie si le commentaire a été modifié"""
        return self.updated_at is not None and self.updated_at > self.created_at


class TicketHistoryModel:
    """Modèle d'historique de ticket"""
    
    def __init__(
        self,
        id: int,
        ticket_id: int,
        user_id: int,
        action: str,
        field_name: Optional[str] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.action = action
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value
        self.description = description
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "action": self.action,
            "field_name": self.field_name,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "description": self.description,
            "created_at": self.created_at
        }


class TicketAttachmentModel:
    """Modèle de pièce jointe de ticket"""
    
    def __init__(
        self,
        id: int,
        ticket_id: int,
        file_name: str,
        file_path: str,
        file_size: int = 0,
        mime_type: Optional[str] = None,
        uploaded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.ticket_id = ticket_id
        self.file_name = file_name
        self.file_path = file_path
        self.file_size = file_size
        self.mime_type = mime_type
        self.uploaded_by = uploaded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at
        }


class SLAModel:
    """Modèle de SLA"""
    
    def __init__(
        self,
        id: int,
        name: str,
        priority: str,
        response_time_hours: int = 0,
        resolution_time_hours: int = 0,
        first_response_required: bool = True,
        is_active: bool = True,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.priority = priority
        self.response_time_hours = response_time_hours
        self.resolution_time_hours = resolution_time_hours
        self.first_response_required = first_response_required
        self.is_active = is_active
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "response_time_hours": self.response_time_hours,
            "resolution_time_hours": self.resolution_time_hours,
            "first_response_required": self.first_response_required,
            "is_active": self.is_active,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
