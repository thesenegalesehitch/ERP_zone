"""
Modèle de données pour les employés

Ce module définit le modèle de données pour les employés
dans le module des ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class EmployeeModel:
    """Modèle d'employé"""
    
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        hire_date: Optional[date] = None,
        department_id: Optional[int] = None,
        position: Optional[str] = None,
        employee_type: str = "cdi",
        status: str = "actif",
        salary: Optional[float] = None,
        manager_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.hire_date = hire_date
        self.department_id = department_id
        self.position = position
        self.employee_type = employee_type
        self.status = status
        self.salary = salary
        self.manager_id = manager_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "hire_date": self.hire_date,
            "department_id": self.department_id,
            "position": self.position,
            "employee_type": self.employee_type,
            "status": self.status,
            "salary": self.salary,
            "manager_id": self.manager_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EmployeeModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            hire_date=data.get("hire_date"),
            department_id=data.get("department_id"),
            position=data.get("position"),
            employee_type=data.get("employee_type", "cdi"),
            status=data.get("status", "actif"),
            salary=data.get("salary"),
            manager_id=data.get("manager_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def get_full_name(self) -> str:
        """Retourne le nom complet"""
        return f"{self.first_name} {self.last_name}"
    
    def is_active(self) -> bool:
        """Vérifie si l'employé est actif"""
        return self.status == "actif"
    
    def years_of_service(self) -> int:
        """Calcule les années d'ancienneté"""
        if not self.hire_date:
            return 0
        today = date.today()
        return today.year - self.hire_date.year - ((today.month, today.day) < (self.hire_date.month, self.hire_date.day))


class AttendanceModel:
    """Modèle de présence"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        date: date,
        check_in: Optional[datetime] = None,
        check_out: Optional[datetime] = None,
        status: str = "present",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.date = date
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "date": self.date,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def calculate_hours_worked(self) -> float:
        """Calcule les heures travaillées"""
        if not self.check_in or not self.check_out:
            return 0
        delta = self.check_out - self.check_in
        return delta.total_seconds() / 3600


class LeaveRequestModel:
    """Modèle de demande de congés"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        leave_type: str,
        start_date: date,
        end_date: date,
        total_days: int,
        status: str = "en_attente",
        approved_by: Optional[int] = None,
        approved_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.total_days = total_days
        self.status = status
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "leave_type": self.leave_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_days": self.total_days,
            "status": self.status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_approved(self) -> bool:
        """Vérifie si la demande est approuvée"""
        return self.status == "approuve"


class PayrollModel:
    """Modèle de paie"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        period_start: date,
        period_end: date,
        base_salary: float,
        bonuses: float = 0,
        deductions: float = 0,
        net_salary: float = 0,
        status: str = "en_attente",
        paid_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.period_start = period_start
        self.period_end = period_end
        self.base_salary = base_salary
        self.bonuses = bonuses
        self.deductions = deductions
        self.net_salary = net_salary or (base_salary + bonuses - deductions)
        self.status = status
        self.paid_at = paid_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "base_salary": self.base_salary,
            "bonuses": self.bonuses,
            "deductions": self.deductions,
            "net_salary": self.net_salary,
            "status": self.status,
            "paid_at": self.paid_at,
            "created_at": self.created_at
        }
    
    def is_paid(self) -> bool:
        """Vérifie si la paie est effectuée"""
        return self.status == "paye"
