"""
Modèle de données pour les inscriptions

Ce module définit le modèle de données pour les inscriptions
dans le module de gestion de l'école.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class RegistrationModel:
    """Modèle d'inscription"""
    
    def __init__(
        self,
        id: int,
        student_id: int,
        academic_year: str,
        semester: str = "S1",
        status: str = "en_attente",
        registration_date: date = None,
        level: Optional[str] = None,
        department: Optional[str] = None,
        program: Optional[str] = None,
        is_confirmed: bool = False,
        confirmed_by: Optional[int] = None,
        confirmed_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.student_id = student_id
        self.academic_year = academic_year
        self.semester = semester
        self.status = status
        self.registration_date = registration_date or date.today()
        self.level = level
        self.department = department
        self.program = program
        self.is_confirmed = is_confirmed
        self.confirmed_by = confirmed_by
        self.confirmed_date = confirmed_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "academic_year": self.academic_year,
            "semester": self.semester,
            "status": self.status,
            "registration_date": self.registration_date,
            "level": self.level,
            "department": self.department,
            "program": self.program,
            "is_confirmed": self.is_confirmed,
            "confirmed_by": self.confirmed_by,
            "confirmed_date": self.confirmed_date,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RegistrationModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            student_id=data.get("student_id"),
            academic_year=data.get("academic_year"),
            semester=data.get("semester", "S1"),
            status=data.get("status", "en_attente"),
            registration_date=data.get("registration_date"),
            level=data.get("level"),
            department=data.get("department"),
            program=data.get("program"),
            is_confirmed=data.get("is_confirmed", False),
            confirmed_by=data.get("confirmed_by"),
            confirmed_date=data.get("confirmed_date"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_confirmed_status(self) -> bool:
        """Vérifie si confirmée"""
        return self.is_confirmed
    
    def is_pending(self) -> bool:
        """Vérifie si en attente"""
        return self.status == "en_attente"


class CourseEnrollmentModel:
    """Modèle d'inscription à un cours"""
    
    def __init__(
        self,
        id: int,
        registration_id: int,
        course_id: int,
        enrollment_date: date = None,
        status: str = "actif",
        is_optional: bool = False,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.registration_id = registration_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date or date.today()
        self.status = status
        self.is_optional = is_optional
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "registration_id": self.registration_id,
            "course_id": self.course_id,
            "enrollment_date": self.enrollment_date,
            "status": self.status,
            "is_optional": self.is_optional,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"


class TuitionModel:
    """Modèle de frais de scolarité"""
    
    def __init__(
        self,
        id: int,
        registration_id: int,
        amount: float = 0,
        currency: str = "XOF",
        due_date: date = None,
        paid_amount: float = 0,
        status: str = "en_attente",
        payment_date: Optional[date] = None,
        payment_method: Optional[str] = None,
        reference: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.registration_id = registration_id
        self.amount = amount
        self.currency = currency
        self.due_date = due_date
        self.paid_amount = paid_amount
        self.status = status
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.reference = reference
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "registration_id": self.registration_id,
            "amount": self.amount,
            "currency": self.currency,
            "due_date": self.due_date,
            "paid_amount": self.paid_amount,
            "status": self.status,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "reference": self.reference,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def balance(self) -> float:
        """Reste à payer"""
        return self.amount - self.paid_amount
    
    def is_paid(self) -> bool:
        """Vérifie si payé"""
        return self.paid_amount >= self.amount
    
    def is_overdue(self) -> bool:
        """Vérifie si en retard"""
        if not self.due_date or self.is_paid():
            return False
        return date.today() > self.due_date
