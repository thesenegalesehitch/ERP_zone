"""
Modèle de données pour les congés

Ce module définit le modèle de données pour les congés
dans le module des ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class LeaveTypeModel:
    """Modèle de type de congé"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        days_per_year: int = 0,
        requires_approval: bool = True,
        is_paid: bool = True,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.days_per_year = days_per_year
        self.requires_approval = requires_approval
        self.is_paid = is_paid
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "days_per_year": self.days_per_year,
            "requires_approval": self.requires_approval,
            "is_paid": self.is_paid,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LeaveTypeModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            code=data.get("code"),
            description=data.get("description"),
            days_per_year=data.get("days_per_year", 0),
            requires_approval=data.get("requires_approval", True),
            is_paid=data.get("is_paid", True),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


class LeaveBalanceModel:
    """Modèle de solde de congés"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        leave_type_id: int,
        year: int,
        days_available: float = 0,
        days_taken: float = 0,
        days_pending: float = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.leave_type_id = leave_type_id
        self.year = year
        self.days_available = days_available
        self.days_taken = days_taken
        self.days_pending = days_pending
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "leave_type_id": self.leave_type_id,
            "year": self.year,
            "days_available": self.days_available,
            "days_taken": self.days_taken,
            "days_pending": self.days_pending,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def remaining_days(self) -> float:
        """Calcule les jours restants"""
        return self.days_available - self.days_taken - self.days_pending
    
    def can_take(self, days: float) -> bool:
        """Vérifie si l'employé peut prendre ces jours"""
        return self.remaining_days() >= days


class LeaveRequestModel:
    """Modèle de demande de congé"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        leave_type_id: int,
        start_date: date,
        end_date: date,
        total_days: float,
        reason: Optional[str] = None,
        status: str = "en_attente",
        approved_by: Optional[int] = None,
        approved_at: Optional[datetime] = None,
        rejected_by: Optional[int] = None,
        rejected_reason: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.leave_type_id = leave_type_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_days = total_days
        self.reason = reason
        self.status = status
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.rejected_by = rejected_by
        self.rejected_reason = rejected_reason
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "leave_type_id": self.leave_type_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_days": self.total_days,
            "reason": self.reason,
            "status": self.status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "rejected_by": self.rejected_by,
            "rejected_reason": self.rejected_reason,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_approved(self) -> bool:
        """Vérifie si la demande est approuvée"""
        return self.status == "approuve"
    
    def is_rejected(self) -> bool:
        """Vérifie si la demande est rejetée"""
        return self.status == "rejete"
    
    def is_pending(self) -> bool:
        """Vérifie si la demande est en attente"""
        return self.status == "en_attente"


class HolidayModel:
    """Modèle de jour férié"""
    
    def __init__(
        self,
        id: int,
        name: str,
        date: date,
        is_recurring: bool = True,
        country: str = "Sénégal",
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.date = date
        self.is_recurring = is_recurring
        self.country = country
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "is_recurring": self.is_recurring,
            "country": self.country,
            "is_active": self.is_active,
            "created_at": self.created_at
        }
