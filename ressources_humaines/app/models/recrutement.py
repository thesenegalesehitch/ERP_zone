"""
Modèle de données pour le recrutement

Ce module définit le modèle de données pour le recrutement
dans le module des ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class JobPositionModel:
    """Modèle de poste à pourvoir"""
    
    def __init__(
        self,
        id: int,
        title: str,
        department: str,
        description: Optional[str] = None,
        position_type: str = "cdi",
        status: str = "ouverte",
        location: Optional[str] = None,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        currency: str = "XOF",
        required_skills: Optional[str] = None,
        experience_required: Optional[int] = None,
        qualifications: Optional[str] = None,
        publication_date: Optional[date] = None,
        closing_date: Optional[date] = None,
        hiring_manager: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.department = department
        self.description = description
        self.position_type = position_type
        self.status = status
        self.location = location
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.required_skills = required_skills
        self.experience_required = experience_required
        self.qualifications = qualifications
        self.publication_date = publication_date
        self.closing_date = closing_date
        self.hiring_manager = hiring_manager
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "title": self.title,
            "department": self.department,
            "description": self.description,
            "position_type": self.position_type,
            "status": self.status,
            "location": self.location,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "currency": self.currency,
            "required_skills": self.required_skills,
            "experience_required": self.experience_required,
            "qualifications": self.qualifications,
            "publication_date": self.publication_date,
            "closing_date": self.closing_date,
            "hiring_manager": self.hiring_manager,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "JobPositionModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            title=data.get("title"),
            department=data.get("department"),
            description=data.get("description"),
            position_type=data.get("position_type", "cdi"),
            status=data.get("status", "ouverte"),
            location=data.get("location"),
            salary_min=data.get("salary_min"),
            salary_max=data.get("salary_max"),
            currency=data.get("currency", "XOF"),
            required_skills=data.get("required_skills"),
            experience_required=data.get("experience_required"),
            qualifications=data.get("qualifications"),
            publication_date=data.get("publication_date"),
            closing_date=data.get("closing_date"),
            hiring_manager=data.get("hiring_manager"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_open(self) -> bool:
        """Vérifie si ouvert"""
        return self.status == "ouverte"
    
    def is_closed(self) -> bool:
        """Vérifie si fermé"""
        return self.status == "fermee"


class CandidateModel:
    """Modèle de candidat"""
    
    def __init__(
        self,
        id: int,
        position_id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        current_company: Optional[str] = None,
        current_position: Optional[str] = None,
        experience_years: int = 0,
        expected_salary: Optional[float] = None,
        status: str = "nouveau",
        source: Optional[str] = None,
        cv_url: Optional[str] = None,
        cover_letter_url: Optional[str] = None,
        notes: Optional[str] = None,
        applied_date: date = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.position_id = position_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.current_company = current_company
        self.current_position = current_position
        self.experience_years = experience_years
        self.expected_salary = expected_salary
        self.status = status
        self.source = source
        self.cv_url = cv_url
        self.cover_letter_url = cover_letter_url
        self.notes = notes
        self.applied_date = applied_date or date.today()
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "position_id": self.position_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "current_company": self.current_company,
            "current_position": self.current_position,
            "experience_years": self.experience_years,
            "expected_salary": self.expected_salary,
            "status": self.status,
            "source": self.source,
            "cv_url": self.cv_url,
            "cover_letter_url": self.cover_letter_url,
            "notes": self.notes,
            "applied_date": self.applied_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"


class InterviewModel:
    """Modèle d'entretien"""
    
    def __init__(
        self,
        id: int,
        candidate_id: int,
        interview_type: str = "telephonique",
        scheduled_date: datetime = None,
        duration_minutes: int = 60,
        location: Optional[str] = None,
        interviewers: Optional[str] = None,
        status: str = "planifie",
        result: Optional[str] = None,
        feedback: Optional[str] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.candidate_id = candidate_id
        self.interview_type = interview_type
        self.scheduled_date = scheduled_date
        self.duration_minutes = duration_minutes
        self.location = location
        self.interviewers = interviewers
        self.status = status
        self.result = result
        self.feedback = feedback
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "interview_type": self.interview_type,
            "scheduled_date": self.scheduled_date,
            "duration_minutes": self.duration_minutes,
            "location": self.location,
            "interviewers": self.interviewers,
            "status": self.status,
            "result": self.result,
            "feedback": self.feedback,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "termine"
