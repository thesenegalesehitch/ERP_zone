"""
Modèle de données pour la gestion des présences

Ce module définit le modèle de données pour les présences
dans le module des ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date, time
from typing import Optional


class AttendanceModel:
    """Modèle de présence"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        date: date = None,
        check_in: Optional[time] = None,
        check_out: Optional[time] = None,
        status: str = "present",
        work_hours: float = 0,
        overtime_hours: float = 0,
        late_minutes: int = 0,
        notes: Optional[str] = None,
        recorded_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.date = date or date.today()
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.work_hours = work_hours
        self.overtime_hours = overtime_hours
        self.late_minutes = late_minutes
        self.notes = notes
        self.recorded_by = recorded_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "date": self.date,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "status": self.status,
            "work_hours": self.work_hours,
            "overtime_hours": self.overtime_hours,
            "late_minutes": self.late_minutes,
            "notes": self.notes,
            "recorded_by": self.recorded_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AttendanceModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            employee_id=data.get("employee_id"),
            date=data.get("date"),
            check_in=data.get("check_in"),
            check_out=data.get("check_out"),
            status=data.get("status", "present"),
            work_hours=data.get("work_hours", 0),
            overtime_hours=data.get("overtime_hours", 0),
            late_minutes=data.get("late_minutes", 0),
            notes=data.get("notes"),
            recorded_by=data.get("recorded_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_work_hours(self) -> float:
        """Calcule les heures de travail"""
        if not self.check_in or not self.check_out:
            return 0
        from datetime import datetime, timedelta
        start = datetime.combine(date.today(), self.check_in)
        end = datetime.combine(date.today(), self.check_out)
        delta = end - start
        return delta.seconds / 3600
    
    def is_present(self) -> bool:
        """Vérifie si présent"""
        return self.status == "present"
    
    def is_late(self) -> bool:
        """Vérifie si en retard"""
        return self.late_minutes > 0


class LeaveModel:
    """Modèle de congé"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        leave_type: str,
        start_date: date,
        end_date: date,
        days_count: float = 0,
        status: str = "en_attente",
        reason: Optional[str] = None,
        approval_date: Optional[date] = None,
        approved_by: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.days_count = days_count
        self.status = status
        self.reason = reason
        self.approval_date = approval_date
        self.approved_by = approved_by
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "leave_type": self.leave_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "days_count": self.days_count,
            "status": self.status,
            "reason": self.reason,
            "approval_date": self.approval_date,
            "approved_by": self.approved_by,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_days(self) -> float:
        """Calcule le nombre de jours"""
        delta = self.end_date - self.start_date
        return delta.days + 1
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"


class LeaveBalanceModel:
    """Modèle de solde de congés"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        leave_type: str,
        year: int,
        total_days: float = 0,
        used_days: float = 0,
        remaining_days: float = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.leave_type = leave_type
        self.year = year
        self.total_days = total_days
        self.used_days = used_days
        self.remaining_days = remaining_days
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "leave_type": self.leave_type,
            "year": self.year,
            "total_days": self.total_days,
            "used_days": self.used_days,
            "remaining_days": self.remaining_days,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def update_balance(self) -> float:
        """Met à jour le solde"""
        self.remaining_days = self.total_days - self.used_days
        return self.remaining_days
