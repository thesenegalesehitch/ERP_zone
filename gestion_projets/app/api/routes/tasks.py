"""
API Routes pour les tâches

Ce module définit les routes API pour la gestion des tâches.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/tasks", tags=["tasks"])


# Mock data pour les tests
MOCK_TASKS = [
    {
        "id": 1,
        "project_id": 1,
        "title": "Conception du projet",
        "description": "Phase de conception initiale",
        "assignee_id": 1,
        "status": "terminee",
        "priority": "haute",
        "estimated_hours": 40,
        "actual_hours": 35,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 2,
        "project_id": 1,
        "title": "Développement API",
        "description": "Développement des endpoints API",
        "assignee_id": 2,
        "status": "en_cours",
        "priority": "haute",
        "estimated_hours": 80,
        "actual_hours": 40,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_tasks(
    project_id: int = None,
    assignee_id: int = None,
    status: str = None
):
    """Récupère la liste des tâches"""
    tasks = MOCK_TASKS
    
    if project_id:
        tasks = [t for t in tasks if t["project_id"] == project_id]
    if assignee_id:
        tasks = [t for t in tasks if t.get("assignee_id") == assignee_id]
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    
    return {"tasks": tasks, "total": len(tasks)}


@router.get("/{task_id}")
async def get_task(task_id: int):
    """Récupère une tâche par son ID"""
    for task in MOCK_TASKS:
        if task["id"] == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Tâche non trouvée")


@router.post("/")
async def create_task(task_data: dict):
    """Crée une nouvelle tâche"""
    new_task = {
        "id": len(MOCK_TASKS) + 1,
        **task_data,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_TASKS.append(new_task)
    return new_task


@router.put("/{task_id}")
async def update_task(task_id: int, task_data: dict):
    """Met à jour une tâche"""
    for i, task in enumerate(MOCK_TASKS):
        if task["id"] == task_id:
            MOCK_TASKS[i] = {
                **task,
                **task_data,
                "updated_at": datetime.now()
            }
            return MOCK_TASKS[i]
    
    raise HTTPException(status_code=404, detail="Tâche non trouvée")


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    """Supprime une tâche"""
    for i, task in enumerate(MOCK_TASKS):
        if task["id"] == task_id:
            MOCK_TASKS.pop(i)
            return {"message": "Tâche supprimée"}
    
    raise HTTPException(status_code=404, detail="Tâche non trouvée")


@router.post("/{task_id}/comments")
async def add_comment(task_id: int, comment: dict):
    """Ajoute un commentaire à une tâche"""
    return {
        "id": 1,
        "task_id": task_id,
        "content": comment.get("content"),
        "created_at": datetime.now()
    }


@router.get("/{task_id}/comments")
async def get_comments(task_id: int):
    """Récupère les commentaires d'une tâche"""
    return {"comments": []}


@router.post("/{task_id}/attachments")
async def upload_attachment(task_id: int, attachment: dict):
    """Télécharge une pièce jointe"""
    return {
        "id": 1,
        "task_id": task_id,
        "filename": attachment.get("filename"),
        "created_at": datetime.now()
    }
