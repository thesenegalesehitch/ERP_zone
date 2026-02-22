"""
Modèle de données pour les SLA

Ce module définit le modèle de données pour les SLA
dans le module de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class SLAModel:
    """Modèle de SLA"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        priority: str,
        first_response_time: int = 0,
        resolution_time: int = 0,
        response_time_unit: str = "heures",
        resolution_time_unit: str = "heures",
        is_business_hours: bool = False,
        escalate_to: Optional[int] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.priority = priority
        self.first_response_time = first_response_time
        self.resolution_time = resolution_time
        self.response_time_unit = response_time_unit
        self.resolution_time_unit = resolution_time_unit
        self.is_business_hours = is_business_hours
        self.escalate_to = escalate_to
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "first_response_time": self.first_response_time,
            "resolution_time": self.resolution_time,
            "response_time_unit": self.response_time_unit,
            "resolution_time_unit": self.resolution_time_unit,
            "is_business_hours": self.is_business_hours,
            "escalate_to": self.escalate_to,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SLAModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            description=data.get("description"),
            priority=data.get("priority"),
            first_response_time=data.get("first_response_time", 0),
            resolution_time=data.get("resolution_time", 0),
            response_time_unit=data.get("response_time_unit", "heures"),
            resolution_time_unit=data.get("resolution_time_unit", "heures"),
            is_business_hours=data.get("is_business_hours", False),
            escalate_to=data.get("escalate_to"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si le SLA est actif"""
        return self.is_active


class TicketSlaModel:
    """Modèle de SLA de ticket"""
    
    def __init__(
        self,
        id: int,
        ticket_id: int,
        sla_id: int,
        first_response_deadline: Optional[datetime] = None,
        resolution_deadline: Optional[datetime] = None,
        first_response_met: bool = False,
        first_response_at: Optional[datetime] = None,
        resolution_met: bool = False,
        resolution_at: Optional[datetime] = None,
        paused_at: Optional[datetime] = None,
        resumed_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.ticket_id = ticket_id
        self.sla_id = sla_id
        self.first_response_deadline = first_response_deadline
        self.resolution_deadline = resolution_deadline
        self.first_response_met = first_response_met
        self.first_response_at = first_response_at
        self.resolution_met = resolution_met
        self.resolution_at = resolution_at
        self.paused_at = paused_at
        self.resumed_at = resumed_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "sla_id": self.sla_id,
            "first_response_deadline": self.first_response_deadline,
            "resolution_deadline": self.resolution_deadline,
            "first_response_met": self.first_response_met,
            "first_response_at": self.first_response_at,
            "resolution_met": self.resolution_met,
            "resolution_at": self.resolution_at,
            "paused_at": self.paused_at,
            "resumed_at": self.resumed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_breached(self) -> bool:
        """Vérifie si le SLA est enfreint"""
        now = datetime.now()
        if not self.first_response_met and self.first_response_deadline:
            if now > self.first_response_deadline:
                return True
        if not self.resolution_met and self.resolution_deadline:
            if now > self.resolution_deadline:
                return True
        return False
    
    def mark_first_response(self):
        """Marque la première réponse"""
        self.first_response_met = True
        self.first_response_at = datetime.now()
    
    def mark_resolution(self):
        """Marque la résolution"""
        self.resolution_met = True
        self.resolution_at = datetime.now()


class KnowledgeBaseCategoryModel:
    """Modèle de catégorie de base de connaissances"""
    
    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None,
        display_order: int = 0,
        is_active: bool = True,
        article_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.parent_id = parent_id
        self.display_order = display_order
        self.is_active = is_active
        self.article_count = article_count
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "parent_id": self.parent_id,
            "display_order": self.display_order,
            "is_active": self.is_active,
            "article_count": self.article_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class EmailTemplateModel:
    """Modèle de modèle d'email"""
    
    def __init__(
        self,
        id: int,
        name: str,
        subject: str,
        body: str,
        template_type: str = "general",
        is_active: bool = True,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.subject = subject
        self.body = body
        self.template_type = template_type
        self.is_active = is_active
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "subject": self.subject,
            "body": self.body,
            "template_type": self.template_type,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def render(self, variables: dict) -> tuple:
        """Rend le modèle avec les variables"""
        subject = self.subject
        body = self.body
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))
        return subject, body
