"""
Modèle de données pour les formations

Ce module définit le modèle de données pour les formations
dans le module des ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class TrainingModel:
    """Modèle de formation"""
    
    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str] = None,
        training_type: str = "interne",
        provider: Optional[str] = None,
        start_date: date = None,
        end_date: Optional[date] = None,
        duration_hours: float = 0,
        location: Optional[str] = None,
        cost: float = 0,
        currency: str = "XOF",
        status: str = "planifie",
        max_participants: int = 20,
        prerequisites: Optional[str] = None,
        objectives: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.training_type = training_type
        self.provider = provider
        self.start_date = start_date or date.today()
        self.end_date = end_date
        self.duration_hours = duration_hours
        self.location = location
        self.cost = cost
        self.currency = currency
        self.status = status
        self.max_participants = max_participants
        self.prerequisites = prerequisites
        self.objectives = objectives
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "training_type": self.training_type,
            "provider": self.provider,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "duration_hours": self.duration_hours,
            "location": self.location,
            "cost": self.cost,
            "currency": self.currency,
            "status": self.status,
            "max_participants": self.max_participants,
            "prerequisites": self.prerequisites,
            "objectives": self.objectives,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TrainingModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            title=data.get("title"),
            description=data.get("description"),
            training_type=data.get("training_type", "interne"),
            provider=data.get("provider"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            duration_hours=data.get("duration_hours", 0),
            location=data.get("location"),
            cost=data.get("cost", 0),
            currency=data.get("currency", "XOF"),
            status=data.get("status", "planifie"),
            max_participants=data.get("max_participants", 20),
            prerequisites=data.get("prerequisites"),
            objectives=data.get("objectives"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si terminée"""
        return self.status == "terminee"
    
    def is_ongoing(self) -> bool:
        """Vérifie si en cours"""
        return self.status == "en_cours"


class TrainingEnrollmentModel:
    """Modèle d'inscription à une formation"""
    
    def __init__(
        self,
        id: int,
        training_id: int,
        employee_id: int,
        enrollment_date: date = None,
        status: str = "inscrit",
        completion_date: Optional[date] = None,
        score: Optional[float] = None,
        grade: Optional[str] = None,
        feedback: Optional[str] = None,
        certificate_url: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.training_id = training_id
        self.employee_id = employee_id
        self.enrollment_date = enrollment_date or date.today()
        self.status = status
        self.completion_date = completion_date
        self.score = score
        self.grade = grade
        self.feedback = feedback
        self.certificate_url = certificate_url
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "training_id": self.training_id,
            "employee_id": self.employee_id,
            "enrollment_date": self.enrollment_date,
            "status": self.status,
            "completion_date": self.completion_date,
            "score": self.score,
            "grade": self.grade,
            "feedback": self.feedback,
            "certificate_url": self.certificate_url,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "termine"


class TrainerModel:
    """Modèle de formateur"""
    
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        expertise: Optional[str] = None,
        bio: Optional[str] = None,
        is_internal: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.company = company
        self.expertise = expertise
        self.bio = bio
        self.is_internal = is_internal
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "expertise": self.expertise,
            "bio": self.bio,
            "is_internal": self.is_internal,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"
