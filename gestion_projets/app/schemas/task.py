"""
Schémas de validation pour les tâches

Ce module définit les schémas Pydantic pour la validation
des données liées aux tâches.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Schéma de base pour une tâche"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field(default="moyenne")
    estimated_hours: Optional[float] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schéma pour créer une tâche"""
    project_id: int
    assignee_id: Optional[int] = None
    parent_task_id: Optional[int] = None


class TaskUpdate(BaseModel):
    """Schéma pour mettre à jour une tâche"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schéma pour la réponse d'une tâche"""
    id: int
    project_id: int
    assignee_id: Optional[int] = None
    status: str
    actual_hours: Optional[float] = None
    completion_date: Optional[datetime] = None
    parent_task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskCommentCreate(BaseModel):
    """Schéma pour créer un commentaire"""
    task_id: int
    content: str = Field(..., min_length=1)


class TaskCommentResponse(BaseModel):
    """Schéma pour la réponse d'un commentaire"""
    id: int
    task_id: int
    user_id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TaskAttachmentCreate(BaseModel):
    """Schéma pour télécharger une pièce jointe"""
    task_id: int
    filename: str
    file_path: str
    file_size: int


class TaskAttachmentResponse(BaseModel):
    """Schéma pour la réponse d'une pièce jointe"""
    id: int
    task_id: int
    filename: str
    file_path: str
    file_size: int
    uploaded_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TaskFilter(BaseModel):
    """Schéma pour filtrer les tâches"""
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
