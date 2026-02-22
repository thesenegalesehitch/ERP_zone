"""
Schémas de validation pour les projets

Ce module définit les schémas Pydantic pour la validation
des données liées aux projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProjectBase(BaseModel):
    """Schéma de base pour un projet"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    """Schéma pour créer un projet"""
    client_id: Optional[int] = None
    manager_id: int
    status: str = Field(default="planifie")


class ProjectUpdate(BaseModel):
    """Schéma pour mettre à jour un projet"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    completion_percent: Optional[int] = None


class ProjectResponse(ProjectBase):
    """Schéma pour la réponse d'un projet"""
    id: int
    client_id: Optional[int] = None
    manager_id: int
    status: str
    completion_percent: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectMemberCreate(BaseModel):
    """Schéma pour ajouter un membre au projet"""
    project_id: int
    user_id: int
    role: str = Field(default="membre")


class ProjectMemberResponse(BaseModel):
    """Schéma pour la réponse d'un membre de projet"""
    id: int
    project_id: int
    user_id: int
    role: str
    joined_at: datetime
    
    class Config:
        from_attributes = True


class MilestoneBase(BaseModel):
    """Schéma de base pour un jalon"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class MilestoneCreate(MilestoneBase):
    """Schéma pour créer un jalon"""
    project_id: int


class MilestoneUpdate(BaseModel):
    """Schéma pour mettre à jour un jalon"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class MilestoneResponse(MilestoneBase):
    """Schéma pour la réponse d'un jalon"""
    id: int
    project_id: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectFilter(BaseModel):
    """Schéma pour filtrer les projets"""
    status: Optional[str] = None
    manager_id: Optional[int] = None
    client_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectStats(BaseModel):
    """Schéma pour les statistiques d'un projet"""
    project_id: int
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    overdue_tasks: int
    total_members: int
    completion_percent: float
    
    class Config:
        from_attributes = True
