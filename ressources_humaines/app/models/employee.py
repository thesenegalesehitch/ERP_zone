"""
Modèle de données pour les employés

Ce module définit le modèle de données pour les employés
dans le module de ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class EmployeeModel:
    """Modèle d'employé"""
    
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        department_id: int,
        position: str,
        salary: float,
        hire_date: datetime,
        contract_type: str = "cdi",
        status: str = "actif",
        phone: Optional[str] = None,
        address: Optional[str] = None,
        manager_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department_id = department_id
        self.position = position
        self.salary = salary
        self.hire_date = hire_date
        self.contract_type = contract_type
        self.status = status
        self.phone = phone
        self.address = address
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
            "department_id": self.department_id,
            "position": self.position,
            "salary": self.salary,
            "hire_date": self.hire_date,
            "contract_type": self.contract_type,
            "status": self.status,
            "phone": self.phone,
            "address": self.address,
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
            department_id=data.get("department_id"),
            position=data.get("position"),
            salary=data.get("salary"),
            hire_date=data.get("hire_date"),
            contract_type=data.get("contract_type", "cdi"),
            status=data.get("status", "actif"),
            phone=data.get("phone"),
            address=data.get("address"),
            manager_id=data.get("manager_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def full_name(self) -> str:
        """Retourne le nom complet"""
        return f"{self.first_name} {self.last_name}"
    
    def years_of_service(self) -> float:
        """Calcule les années d'ancienneté"""
        delta = datetime.now() - self.hire_date
        return delta.days / 365.25
    
    def is_active(self) -> bool:
        """Vérifie si l'employé est actif"""
        return self.status == "actif"


class DepartmentModel:
    """Modèle de département"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        manager_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.manager_id = manager_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "manager_id": self.manager_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class LeaveRequestModel:
    """Modèle de demande de congés"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        leave_type: str,
        start_date: datetime,
        end_date: datetime,
        status: str = "en_attente",
        reason: Optional[str] = None,
        reviewed_by: Optional[int] = None,
        reviewed_at: Optional[datetime] = None,
        comments: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.reason = reason
        self.reviewed_by = reviewed_by
        self.reviewed_at = reviewed_at
        self.comments = comments
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "leave_type": self.leave_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "reason": self.reason,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at,
            "comments": self.comments,
            "created_at": self.created_at
        }
    
    def duration_days(self) -> int:
        """Calcule la durée en jours"""
        return (self.end_date - self.start_date).days + 1
    
    def is_pending(self) -> bool:
        """Vérifie si la demande est en attente"""
        return self.status == "en_attente"
