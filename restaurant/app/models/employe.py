"""
Modèle de données pour les employés du restaurant

Ce module définit le modèle de données pour les employés
dans le module restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class EmployeeModel:
    """Modèle d'employé"""
    
    def __init__(
        self,
        id: int,
        employee_number: str,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        position: str = "serveur",
        department: Optional[str] = None,
        hire_date: Optional[datetime] = None,
        status: str = "actif",
        hourly_rate: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_number = employee_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone =.position = position
 phone
        self        self.department = department
        self.hire_date = hire_date
        self.status = status
        self.hourly_rate = hourly_rate
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_number": self.employee_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "position": self.position,
            "department": self.department,
            "hire_date": self.hire_date,
            "status": self.status,
            "hourly_rate": self.hourly_rate,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EmployeeModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            employee_number=data.get("employee_number"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            position=data.get("position", "serveur"),
            department=data.get("department"),
            hire_date=data.get("hire_date"),
            status=data.get("status", "actif"),
            hourly_rate=data.get("hourly_rate", 0),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"


class ScheduleAssignmentModel:
    """Modèle d'affectation d'horaire"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        shift_date: datetime = None,
        start_time: datetime = None,
        end_time: datetime = None,
        position: Optional[str] = None,
        status: str = "planifie",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.shift_date = shift_date
        self.start_time = start_time
        self.end_time = end_time
        self.position = position
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "shift_date": self.shift_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "position": self.position,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def hours_worked(self) -> float:
        """Heures travaillées"""
        if not self.start_time or not self.end_time:
            return 0
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600


class TimeClockModel:
    """Modèle de pointage"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        clock_in: datetime = None,
        clock_out: Optional[datetime] = None,
        break_minutes: int = 0,
        total_hours: float = 0,
        date: datetime = None,
        status: str = "en_cours",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.clock_in = clock_in
        self.clock_out = clock_out
        self.break_minutes = break_minutes
        self.total_hours = total_hours
        self.date = date
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "clock_in": self.clock_in,
            "clock_out": self.clock_out,
            "break_minutes": self.break_minutes,
            "total_hours": self.total_hours,
            "date": self.date,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def calculate_hours(self):
        """Calcule les heures"""
        if self.clock_in and self.clock_out:
            delta = self.clock_out - self.clock_in
            self.total_hours = (delta.total_seconds() / 3600) - (self.break_minutes / 60)
    
    def is_clocked_in(self) -> bool:
        """Vérifie si pointé"""
        return self.clock_in is not None and self.clock_out is None
