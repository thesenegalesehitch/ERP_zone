"""
API Routes pour les projets

Ce module définit les routes API pour la gestion des projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/projects", tags=["projects"])


# Mock data pour les tests
MOCK_PROJECTS = [
    {
        "id": 1,
        "name": "ERP Senegal",
        "description": "Système ERP pour entreprise sénégalaise",
        "client_id": 1,
        "manager_id": 1,
        "status": "en_cours",
        "budget": 5000000,
        "completion_percent": 45,
        "start_date": datetime.now(),
        "end_date": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_projects(
    status: str = None,
    manager_id: int = None
):
    """Récupère la liste des projets"""
    projects = MOCK_PROJECTS
    
    if status:
        projects = [p for p in projects if p["status"] == status]
    if manager_id:
        projects = [p for p in projects if p["manager_id"] == manager_id]
    
    return {"projects": projects, "total": len(projects)}


@router.get("/{project_id}")
async def get_project(project_id: int):
    """Récupère un projet par son ID"""
    for project in MOCK_PROJECTS:
        if project["id"] == project_id:
            return project
    
    raise HTTPException(status_code=404, detail="Projet non trouvé")


@router.post("/")
async def create_project(project_data: dict):
    """Crée un nouveau projet"""
    new_project = {
        "id": len(MOCK_PROJECTS) + 1,
        **project_data,
        "status": project_data.get("status", "planifie"),
        "completion_percent": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_PROJECTS.append(new_project)
    return new_project


@router.put("/{project_id}")
async def update_project(project_id: int, project_data: dict):
    """Met à jour un projet"""
    for i, project in enumerate(MOCK_PROJECTS):
        if project["id"] == project_id:
            MOCK_PROJECTS[i] = {
                **project,
                **project_data,
                "updated_at": datetime.now()
            }
            return MOCK_PROJECTS[i]
    
    raise HTTPException(status_code=404, detail="Projet non trouvé")


@router.delete("/{project_id}")
async def delete_project(project_id: int):
    """Supprime un projet"""
    for i, project in enumerate(MOCK_PROJECTS):
        if project["id"] == project_id:
            MOCK_PROJECTS.pop(i)
            return {"message": "Projet supprimé"}
    
    raise HTTPException(status_code=404, detail="Projet non trouvé")


@router.get("/{project_id}/tasks")
async def get_project_tasks(project_id: int):
    """Récupère les tâches d'un projet"""
    return {"tasks": [], "total": 0}


@router.get("/{project_id}/members")
async def get_project_members(project_id: int):
    """Récupère les membres d'un projet"""
    return {"members": [], "total": 0}


@router.post("/{project_id}/members")
async def add_project_member(project_id: int, member_data: dict):
    """Ajoute un membre au projet"""
    return {
        "id": 1,
        "project_id": project_id,
        "user_id": member_data.get("user_id"),
        "role": member_data.get("role", "membre"),
        "joined_at": datetime.now()
    }


@router.get("/{project_id}/milestones")
async def get_project_milestones(project_id: int):
    """Récupère les jalons d'un projet"""
    return {"milestones": [], "total": 0}


@router.post("/{project_id}/milestones")
async def create_milestone(project_id: int, milestone_data: dict):
    """Crée un jalon"""
    return {
        "id": 1,
        "project_id": project_id,
        **milestone_data,
        "is_completed": False,
        "created_at": datetime.now()
    }


@router.get("/{project_id}/stats")
async def get_project_stats(project_id: int):
    """Récupère les statistiques d'un projet"""
    return {
        "total_tasks": 10,
        "completed_tasks": 4,
        "in_progress_tasks": 3,
        "overdue_tasks": 1,
        "total_members": 5,
        "completion_percent": 45
    }
