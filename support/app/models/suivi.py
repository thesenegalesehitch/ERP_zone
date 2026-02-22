"""
Modèle de données pour le suivi des tickets

Ce module définit le modèle de données pour le suivi
dans le module de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class TicketHistoryModel:
    """Modèle d'historique de ticket"""
    
    def __init__(
        self,
        id: int,
        ticket_id: int,
        field_changed: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        changed_by: int = None,
        changed_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.ticket_id = ticket_id
        self.field_changed = field_changed
        self.old_value = old_value
        self.new_value = new_value
        self.changed_by = changed_by
        self.changed_at = changed_at
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "field_changed": self.field_changed,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "changed_by": self.changed_by,
            "changed_at": self.changed_at,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TicketHistoryModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            ticket_id=data.get("ticket_id"),
            field_changed=data.get("field_changed"),
            old_value=data.get("old_value"),
            new_value=data.get("new_value"),
            changed_by=data.get("changed_by"),
            changed_at=data.get("changed_at"),
            notes=data.get("notes"),
            created_at=data.get("created_at")
        )


class TicketAttachmentModel:
    """Modèle de pièce jointe"""
    
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
    
    def file_size_mb(self) -> float:
        """Taille en MB"""
        return self.file_size / (1024 * 1024)


class TicketFeedbackModel:
    """Modèle de feedback de ticket"""
    
    def __init__(
        self,
        id: int,
        ticket_id: int,
        rating: int = 0,
        feedback_type: str = "resolution",
        comments: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.ticket_id = ticket_id
        self.rating = rating
        self.feedback_type = feedback_type
        self.comments = comments
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "rating": self.rating,
            "feedback_type": self.feedback_type,
            "comments": self.comments,
            "created_at": self.created_at
        }
    
    def is_satisfied(self) -> bool:
        """Vérifie si satisfait"""
        return self.rating >= 4
