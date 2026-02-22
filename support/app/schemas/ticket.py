"""
Schémas de validation pour les tickets

Ce module définit les schémas Pydantic pour la validation
des données liées aux tickets de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TicketBase(BaseModel):
    """Schéma de base pour un ticket"""
    subject: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class TicketCreate(TicketBase):
    """Schéma pour créer un ticket"""
    ticket_type: str = Field(default="incident")
    priority: str = Field(default="moyenne")
    category: str = Field(default="autre")
    client_id: Optional[int] = None


class TicketUpdate(BaseModel):
    """Schéma pour mettre à jour un ticket"""
    subject: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    assigned_to: Optional[int] = None
    resolved_at: Optional[datetime] = None


class TicketResponse(TicketBase):
    """Schéma pour la réponse d'un ticket"""
    id: int
    ticket_type: str
    priority: str
    category: str
    status: str
    client_id: Optional[int] = None
    assigned_to: Optional[int] = None
    first_response_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TicketCommentCreate(BaseModel):
    """Schéma pour créer un commentaire"""
    ticket_id: int
    content: str = Field(..., min_length=1)
    is_internal: bool = Field(default=False)


class TicketCommentResponse(BaseModel):
    """Schéma pour la réponse d'un commentaire"""
    id: int
    ticket_id: int
    user_id: int
    content: str
    is_internal: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TicketAttachmentCreate(BaseModel):
    """Schéma pour télécharger une pièce jointe"""
    ticket_id: int
    filename: str
    file_path: str
    file_size: int


class TicketAttachmentResponse(BaseModel):
    """Schéma pour la réponse d'une pièce jointe"""
    id: int
    ticket_id: int
    filename: str
    file_path: str
    file_size: int
    uploaded_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class KnowledgeBaseArticleBase(BaseModel):
    """Schéma de base pour un article"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str


class KnowledgeBaseArticleCreate(KnowledgeBaseArticleBase):
    """Schéma pour créer un article"""
    category: str
    tags: Optional[str] = None


class KnowledgeBaseArticleUpdate(BaseModel):
    """Schéma pour mettre à jour un article"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_published: Optional[bool] = None


class KnowledgeBaseArticleResponse(KnowledgeBaseArticleBase):
    """Schéma pour la réponse d'un article"""
    id: int
    category: str
    tags: Optional[str] = None
    is_published: bool
    views: int = 0
    helpful_count: int = 0
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TicketFilter(BaseModel):
    """Schéma pour filtrer les tickets"""
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    assigned_to: Optional[int] = None
    client_id: Optional[int] = None
