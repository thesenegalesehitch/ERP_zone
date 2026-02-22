"""
Modèle de données pour les activités

Ce module définit le modèle de données pour les activités
dans le module de gestion des clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class ActivityModel:
    """Modèle d'activité"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        activity_type: str,
        subject: str,
        description: Optional[str] = None,
        scheduled_date: Optional[datetime] = None,
        completed_date: Optional[datetime] = None,
        status: str = "planifie",
        priority: str = "normale",
        assigned_to: Optional[int] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.activity_type = activity_type
        self.subject = subject
        self.description = description
        self.scheduled_date = scheduled_date
        self.completed_date = completed_date
        self.status = status
        self.priority = priority
        self.assigned_to = assigned_to
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "activity_type": self.activity_type,
            "subject": self.subject,
            "description": self.description,
            "scheduled_date": self.scheduled_date,
            "completed_date": self.completed_date,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ActivityModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            client_id=data.get("client_id"),
            activity_type=data.get("activity_type"),
            subject=data.get("subject"),
            description=data.get("description"),
            scheduled_date=data.get("scheduled_date"),
            completed_date=data.get("completed_date"),
            status=data.get("status", "planifie"),
            priority=data.get("priority", "normale"),
            assigned_to=data.get("assigned_to"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si l'activité est terminée"""
        return self.status == "termine"
    
    def is_overdue(self) -> bool:
        """Vérifie si l'activité est en retard"""
        if not self.scheduled_date or self.is_completed():
            return False
        return datetime.now() > self.scheduled_date


class TaskModel:
    """Modèle de tâche"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[date] = None,
        status: str = "a_faire",
        priority: str = "moyenne",
        assigned_to: Optional[int] = None,
        completed_at: Optional[datetime] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.priority = priority
        self.assigned_to = assigned_to
        self.completed_at = completed_at
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "completed_at": self.completed_at,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def complete(self):
        """Marque la tâche comme terminée"""
        self.status = "termine"
        self.completed_at = datetime.now()
    
    def is_completed(self) -> bool:
        """Vérifie si la tâche est terminée"""
        return self.status == "termine"
    
    def is_overdue(self) -> bool:
        """Vérifie si la tâche est en retard"""
        if not self.due_date or self.is_completed():
            return False
        return date.today() > self.due_date


class ReminderModel:
    """Modèle de rappel"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        reminder_type: str,
        title: str,
        message: Optional[str] = None,
        remind_at: Optional[datetime] = None,
        is_sent: bool = False,
        sent_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.reminder_type = reminder_type
        self.title = title
        self.message = message
        self.remind_at = remind_at
        self.is_sent = is_sent
        self.sent_at = sent_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "reminder_type": self.reminder_type,
            "title": self.title,
            "message": self.message,
            "remind_at": self.remind_at,
            "is_sent": self.is_sent,
            "sent_at": self.sent_at,
            "created_at": self.created_at
        }
    
    def mark_sent(self):
        """Marque le rappel comme envoyé"""
        self.is_sent = True
        self.sent_at = datetime.now()
    
    def should_send(self) -> bool:
        """Vérifie si le rappel doit être envoyé"""
        if self.is_sent or not self.remind_at:
            return False
        return datetime.now() >= self.remind_at


class SalesPipelineModel:
    """Modèle de pipeline de vente"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        opportunity_name: str,
        stage: str = "prospect",
        value: float = 0,
        probability: int = 0,
        expected_close_date: Optional[date] = None,
        actual_close_date: Optional[date] = None,
        status: str = "ouverte",
        notes: Optional[str] = None,
        assigned_to: int = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.opportunity_name = opportunity_name
        self.stage = stage
        self.value = value
        self.probability = probability
        self.expected_close_date = expected_close_date
        self.actual_close_date = actual_close_date
        self.status = status
        self.notes = notes
        self.assigned_to = assigned_to
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "opportunity_name": self.opportunity_name,
            "stage": self.stage,
            "value": self.value,
            "probability": self.probability,
            "expected_close_date": self.expected_close_date,
            "actual_close_date": self.actual_close_date,
            "status": self.status,
            "notes": self.notes,
            "assigned_to": self.assigned_to,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def weighted_value(self) -> float:
        """Calcule la valeur pondérée"""
        return self.value * (self.probability / 100)
    
    def is_won(self) -> bool:
        """Vérifie si l'opportunité est gagnée"""
        return self.status == "gagnee"
    
    def is_lost(self) -> bool:
        """Vérifie si l'opportunité est perdue"""
        return self.status == "perdue"
