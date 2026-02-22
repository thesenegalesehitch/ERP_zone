"""
Schémas de validation pour les livres

Ce module définit les schémas Pydantic pour la validation
des données liées aux livres.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookBase(BaseModel):
    """Schéma de base pour un livre"""
    title: str = Field(..., min_length=1, max_length=300)
    author: str = Field(..., min_length=1, max_length=200)
    isbn: Optional[str] = None


class BookCreate(BookBase):
    """Schéma pour créer un livre"""
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    genre: str
    quantity: int = Field(default=1, ge=0)
    price: float = Field(default=0, ge=0)


class BookUpdate(BaseModel):
    """Schéma pour mettre à jour un livre"""
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)


class BookResponse(BookBase):
    """Schéma pour la réponse d'un livre"""
    id: int
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    genre: str
    quantity: int
    available: int
    price: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LoanCreate(BaseModel):
    """Schéma pour créer un prêt"""
    book_id: int
    member_id: int
    loan_days: int = Field(default=14, ge=1, le=60)


class LoanUpdate(BaseModel):
    """Schéma pour mettre à jour un prêt"""
    status: Optional[str] = None
    return_date: Optional[datetime] = None


class LoanResponse(BaseModel):
    """Schéma pour la réponse d'un prêt"""
    id: int
    book_id: int
    member_id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str
    renewal_count: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    """Schéma de base pour un membre"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None


class MemberCreate(MemberBase):
    """Schéma pour créer un membre"""
    membership_type: str = Field(default="standard")
    id_number: Optional[str] = None


class MemberUpdate(BaseModel):
    """Schéma pour mettre à jour un membre"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    membership_type: Optional[str] = None
    status: Optional[str] = None


class MemberResponse(MemberBase):
    """Schéma pour la réponse d'un membre"""
    id: int
    membership_type: str
    id_number: Optional[str] = None
    status: str
    membership_start: datetime
    membership_end: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FineCreate(BaseModel):
    """Schéma pour créer une amende"""
    loan_id: int
    fine_type: str
    amount: float = Field(..., gt=0)


class FineResponse(BaseModel):
    """Schéma pour la réponse d'une amende"""
    id: int
    loan_id: int
    fine_type: str
    amount: float
    status: str
    paid_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class BookFilter(BaseModel):
    """Schéma pour filtrer les livres"""
    genre: Optional[str] = None
    available_only: Optional[bool] = None
    search: Optional[str] = None


class MemberFilter(BaseModel):
    """Schéma pour filtrer les membres"""
    membership_type: Optional[str] = None
    status: Optional[str] = None
    search: Optional[str] = None
