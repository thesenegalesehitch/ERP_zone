"""
Modèle de données pour les étudiants

Ce module définit le modèle de données pour les étudiants
dans le module de gestion de l'école.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class StudentModel:
    """Modèle d'étudiant"""
    
    def __init__(
        self,
        id: int,
        student_number: str,
        first_name: str,
        last_name: str,
        gender: str,
        birth_date: date,
        birth_place: Optional[str] = None,
        nationality: str = "Sénégalaise",
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        status: str = "actif",
        registration_date: date = None,
        photo_url: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.student_number = student_number
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.nationality = nationality
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.status = status
        self.registration_date = registration_date or date.today()
        self.photo_url = photo_url
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "student_number": self.student_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "birth_date": self.birth_date,
            "birth_place": self.birth_place,
            "nationality": self.nationality,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "status": self.status,
            "registration_date": self.registration_date,
            "photo_url": self.photo_url,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StudentModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            student_number=data.get("student_number"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            gender=data.get("gender"),
            birth_date=data.get("birth_date"),
            birth_place=data.get("birth_place"),
            nationality=data.get("nationality", "Sénégalaise"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            city=data.get("city"),
            status=data.get("status", "actif"),
            registration_date=data.get("registration_date"),
            photo_url=data.get("photo_url"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"
    
    def age(self) -> int:
        """Âge de l'étudiant"""
        today = date.today()
        return today.year - self.birth_date - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"


class ParentModel:
    """Modèle de parent/tuteur"""
    
    def __init__(
        self,
        id: int,
        student_id: int,
        first_name: str,
        last_name: str,
        relationship: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        professional_phone: Optional[str] = None,
        address: Optional[str] = None,
        profession: Optional[str] = None,
        is_emergency_contact: bool = False,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.relationship = relationship
        self.email = email
        self.phone = phone
        self.professional_phone = professional_phone
        self.address = address
        self.profession = profession
        self.is_emergency_contact = is_emergency_contact
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "relationship": self.relationship,
            "email": self.email,
            "phone": self.phone,
            "professional_phone": self.professional_phone,
            "address": self.address,
            "profession": self.profession,
            "is_emergency_contact": self.is_emergency_contact,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"


class StudentAttendanceModel:
    """Modèle de présence étudiant"""
    
    def __init__(
        self,
        id: int,
        student_id: int,
        course_id: int,
        date: date,
        status: str = "present",
        excused: bool = False,
        notes: Optional[str] = None,
        recorded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.date = date
        self.status = status
        self.excused = excused
        self.notes = notes
        self.recorded_by = recorded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "date": self.date,
            "status": self.status,
            "excused": self.excused,
            "notes": self.notes,
            "recorded_by": self.recorded_by,
            "created_at": self.created_at
        }
