"""
API Routes pour les employés

Ce module définit les routes API pour la gestion des employés.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/employees", tags=["employees"])


# Mock data pour les tests
MOCK_EMPLOYEES = [
    {
        "id": 1,
        "first_name": "Moussa",
        "last_name": "Diop",
        "email": "moussa.diop@entreprise.sn",
        "phone": "+221771234567",
        "department_id": 1,
        "position": "Développeur Full Stack",
        "salary": 500000,
        "contract_type": "cdi",
        "status": "actif",
        "hire_date": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_employees(
    department_id: int = None,
    status: str = None,
    search: str = None
):
    """Récupère la liste des employés"""
    employees = MOCK_EMPLOYEES
    
    if department_id:
        employees = [e for e in employees if e["department_id"] == department_id]
    if status:
        employees = [e for e in employees if e["status"] == status]
    if search:
        employees = [e for e in employees if search.lower() in f"{e['first_name']} {e['last_name']}".lower()]
    
    return {"employees": employees, "total": len(employees)}


@router.get("/{employee_id}")
async def get_employee(employee_id: int):
    """Récupère un employé par son ID"""
    for employee in MOCK_EMPLOYEES:
        if employee["id"] == employee_id:
            return employee
    
    raise HTTPException(status_code=404, detail="Employé non trouvé")


@router.post("/")
async def create_employee(employee_data: dict):
    """Crée un nouvel employé"""
    new_employee = {
        "id": len(MOCK_EMPLOYEES) + 1,
        **employee_data,
        "status": "actif",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_EMPLOYEES.append(new_employee)
    return new_employee


@router.put("/{employee_id}")
async def update_employee(employee_id: int, employee_data: dict):
    """Met à jour un employé"""
    for i, employee in enumerate(MOCK_EMPLOYEES):
        if employee["id"] == employee_id:
            MOCK_EMPLOYEES[i] = {
                **employee,
                **employee_data,
                "updated_at": datetime.now()
            }
            return MOCK_EMPLOYEES[i]
    
    raise HTTPException(status_code=404, detail="Employé non trouvé")


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    """Supprime un employé"""
    for i, employee in enumerate(MOCK_EMPLOYEES):
        if employee["id"] == employee_id:
            MOCK_EMPLOYEES.pop(i)
            return {"message": "Employé supprimé"}
    
    raise HTTPException(status_code=404, detail="Employé non trouvé")


@router.get("/{employee_id}/leaves")
async def get_employee_leaves(employee_id: int):
    """Récupère les congés d'un employé"""
    return {"leaves": [], "total": 0}


@router.post("/{employee_id}/leaves")
async def create_leave_request(employee_id: int, leave_data: dict):
    """Crée une demande de congés"""
    return {
        "id": 1,
        "employee_id": employee_id,
        **leave_data,
        "status": "en_attente",
        "created_at": datetime.now()
    }


@router.get("/{employee_id}/attendance")
async def get_employee_attendance(employee_id: int):
    """Récupère la présence d'un employé"""
    return {"records": [], "total": 0}


@router.get("/{employee_id}/evaluations")
async def get_employee_evaluations(employee_id: int):
    """Récupère les évaluations d'un employé"""
    return {"evaluations": [], "total": 0}
