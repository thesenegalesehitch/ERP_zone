"""
Schémas de validation pour les employés

Ce module définit les schémas Pydantic pour la validation
des données liées aux employés.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    """Schéma de base pour un employé"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    address: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    """Schéma pour créer un employé"""
    hire_date: datetime
    department_id: int
    position: str
    salary: float = Field(..., gt=0)
    contract_type: str = Field(default="cdi")
    manager_id: Optional[int] = None


class EmployeeUpdate(BaseModel):
    """Schéma pour mettre à jour un employé"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    address: Optional[str] = None
    department_id: Optional[int] = None
    position: Optional[str] = None
    salary: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    """Schéma pour la réponse d'un employé"""
    id: int
    department_id: int
    position: str
    salary: float
    contract_type: str
    status: str
    hire_date: datetime
    manager_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    """Schéma de base pour un département"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    """Schéma pour créer un département"""
    manager_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    """Schéma pour mettre à jour un département"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    manager_id: Optional[int] = None


class DepartmentResponse(DepartmentBase):
    """Schéma pour la réponse d'un département"""
    id: int
    manager_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LeaveRequestCreate(BaseModel):
    """Schéma pour créer une demande de congés"""
    employee_id: int
    leave_type: str
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None


class LeaveRequestUpdate(BaseModel):
    """Schéma pour mettre à jour une demande de congés"""
    status: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    comments: Optional[str] = None


class LeaveRequestResponse(BaseModel):
    """Schéma pour la réponse d'une demande de congés"""
    id: int
    employee_id: int
    leave_type: str
    start_date: datetime
    end_date: datetime
    status: str
    reason: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    comments: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class EmployeeFilter(BaseModel):
    """Schéma pour filtrer les employés"""
    department_id: Optional[int] = None
    status: Optional[str] = None
    position: Optional[str] = None
    search: Optional[str] = None
