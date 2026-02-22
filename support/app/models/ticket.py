"""
Modèle de données pour les tickets

Ce module définit le modèle de données pour les tickets
dans le module de support client.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class TicketModel:
    """Modèle de ticket"""
    
    def __init__(
        self,
        id: int,
        subject: str,
        ticket_type: str = "incident",
        priority: str = "moyenne",
        category: str = "autre",
        status: str = "nouveau",
        description: Optional[str] = None,
        client_id: Optional[int] = None,
        assigned_to: Optional[int] = None,
        first_response_at: Optional[datetime] = None,
        resolved_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.subject = subject
        self.ticket_type = ticket_type
        self.priority = priority
        self.category = category
        self.status = status
        self.description = description
        self.client_id = client_id
        self.assigned_to = assigned_to
        self.first_response_at = first_response_at
        self.resolved_at = resolved_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "subject": self.subject,
            "ticket_type": self.ticket_type,
            "priority": self.priority,
            "category": self.category,
            "status": self.status,
            "description": self.description,
            "client_id": self.client_id,
            "assigned_to": self.assigned_to,
            "first_response_at": self.first_response_at,
            "resolved_at": self.resolved_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TicketModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            subject=data.get("subject"),
            ticket_type=data.get("ticket_type", "incident"),
            priority=data.get("priority", "moyenne"),
            category=data.get("category", "autre"),
            status=data.get("status", "nouveau"),
            description=data.get("description"),
            client_id=data.get("client_id"),
            assigned_to=data.get("assigned_to"),
            first_response_at=data.get("first_response_at"),
            resolved_at=data.get("resolved_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_resolved(self) -> bool:
        """Vérifie si le ticket est résolu"""
        return self.status in ["resolu", "ferme"]
    
    def is_overdue(self, sla_hours: dict = None) -> bool:
        """Vérifie si le ticket est en retard SLA"""
        if self.is_resolved():
            return False
        
        if sla_hours is None:
            sla_hours = {
                "critique": 4,
                "haute": 24,
                "moyenne": 72,
                "basse": 168
            }
        
        sla = sla_hours.get(self.priority, 72)
        age_hours = (datetime.now() - self.created_at).total_seconds() / 3600
        
        return age_hours > sla


class TicketCommentModel:
    """Modèle de commentaire de ticket"""
    
    def __init__(
        self,
        id: int,
        ticket_id: int,
        user_id: int,
        content: str,
        is_internal: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.content = content
        self.is_internal = is_internal
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "content": self.content,
            "is_internal": self.is_internal,
            "created_at": self.created_at
        }


class KnowledgeBaseArticleModel:
    """Modèle d'article de base de connaissances"""
    
    def __init__(
        self,
        id: int,
        title: str,
        content: str,
        category: str,
        tags: Optional[str] = None,
        is_published: bool = False,
        views: int = 0,
        helpful_count: int = 0,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.content = content
        self.category = category
        self.tags = tags
        self.is_published = is_published
        self.views = views
        self.helpful_count = helpful_count
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "is_published": self.is_published,
            "views": self.views,
            "helpful_count": self.helpful_count,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def increment_views(self):
        """Incrémenter le compteur de vues"""
        self.views += 1
    
    def mark_helpful(self):
        """Marquer comme utile"""
        self.helpful_count += 1
