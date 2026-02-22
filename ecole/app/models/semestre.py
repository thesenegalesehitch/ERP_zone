"""
Modèle de données pour les semestres

Ce module définit le modèle de données pour les semestres
dans le module école.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class SemesterModel:
    """Modèle de semestre"""
    
    def __init__(
        self,
        id: int,
        academic_year_id: int,
        name: str,
        semester_number: int,
        start_date: date,
        end_date: date,
        is_active: bool = True,
        registration_start: Optional[date] = None,
        registration_end: Optional[date] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.academic_year_id = academic_year_id
        self.name = name
        self.semester_number = semester_number
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.registration_start = registration_start
        self.registration_end = registration_end
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "academic_year_id": self.academic_year_id,
            "name": self.name,
            "semester_number": self.semester_number,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "registration_start": self.registration_start,
            "registration_end": self.registration_end,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SemesterModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            academic_year_id=data.get("academic_year_id"),
            name=data.get("name"),
            semester_number=data.get("semester_number"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            is_active=data.get("is_active", True),
            registration_start=data.get("registration_start"),
            registration_end=data.get("registration_end"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active_period(self) -> bool:
        """Vérifie si nous sommes dans la période"""
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def is_registration_open(self) -> bool:
        """Vérifie si les inscriptions sont ouvertes"""
        if not self.registration_start or not self.registration_end:
            return False
        today = date.today()
        return self.registration_start <= today <= self.registration_end


class AcademicYearModel:
    """Modèle d'année académique"""
    
    def __init__(
        self,
        id: int,
        name: str,
        year: str,
        start_date: date,
        end_date: date,
        is_current: bool = False,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.year = year
        self.start_date = start_date
        self.end_date = end_date
        self.is_current = is_current
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_current": self.is_current,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_active_period(self) -> bool:
        """Vérifie si nous sommes dans la période"""
        today = date.today()
        return self.start_date <= today <= self.end_date


class ProgramModel:
    """Modèle de programme"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        duration_years: int = 3,
        degree_type: str = "licence",
        is_active: bool = True,
        department: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.duration_years = duration_years
        self.degree_type = degree_type
        self.is_active = is_active
        self.department = department
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "duration_years": self.duration_years,
            "degree_type": self.degree_type,
            "is_active": self.is_active,
            "department": self.department,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class RoomModel:
    """Modèle de salle"""
    
    def __init__(
        self,
        id: int,
        name: str,
        building: str,
        capacity: int = 30,
        room_type: str = "cours",
        equipment: Optional[str] = None,
        is_available: bool = True,
        floor: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.building = building
        self.capacity = capacity
        self.room_type = room_type
        self.equipment = equipment
        self.is_available = is_available
        self.floor = floor
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "building": self.building,
            "capacity": self.capacity,
            "room_type": self.room_type,
            "equipment": self.equipment,
            "is_available": self.is_available,
            "floor": self.floor,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_available(self) -> bool:
        """Vérifie si la salle est disponible"""
        return self.is_available
