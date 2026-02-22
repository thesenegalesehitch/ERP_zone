"""
Schémas de validation pour les étudiants

Ce module définit les schémas Pydantic pour la validation
des données liées aux étudiants.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class StudentBase(BaseModel):
    """Schéma de base pour un étudiant"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None


class StudentCreate(StudentBase):
    """Schéma pour créer un étudiant"""
    enrollment_date: datetime
    class_id: int
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_email: Optional[str] = None


class StudentUpdate(BaseModel):
    """Schéma pour mettre à jour un étudiant"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None
    status: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_email: Optional[str] = None


class StudentResponse(StudentBase):
    """Schéma pour la réponse d'un étudiant"""
    id: int
    class_id: int
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_email: Optional[str] = None
    status: str
    enrollment_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    """Schéma de base pour un cours"""
    name: str = Field(..., min_length=1, max_length=200)
    code: str = Field(..., min_length=1, max_length=20)
    credits: int = Field(default=3, ge=1)


class CourseCreate(CourseBase):
    """Schéma pour créer un cours"""
    class_id: int
    teacher_id: Optional[int] = None


class CourseUpdate(BaseModel):
    """Schéma pour mettre à jour un cours"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    teacher_id: Optional[int] = None
    credits: Optional[int] = Field(None, ge=1)


class CourseResponse(CourseBase):
    """Schéma pour la réponse d'un cours"""
    id: int
    class_id: int
    teacher_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GradeCreate(BaseModel):
    """Schéma pour créer une note"""
    student_id: int
    course_id: int
    grade_value: float = Field(..., ge=0, le=20)
    grade_type: str = Field(default="devoir")


class GradeResponse(BaseModel):
    """Schéma pour la réponse d'une note"""
    id: int
    student_id: int
    course_id: int
    grade_value: float
    grade_type: str
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AttendanceCreate(BaseModel):
    """Schéma pour enregistrer la présence"""
    student_id: int
    course_id: int
    date: datetime
    status: str = Field(default="present")


class AttendanceResponse(BaseModel):
    """Schéma pour la réponse de présence"""
    id: int
    student_id: int
    course_id: int
    date: datetime
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeeCreate(BaseModel):
    """Schéma pour créer des frais"""
    student_id: int
    fee_type: str
    amount: float = Field(..., gt=0)
    due_date: datetime


class FeeUpdate(BaseModel):
    """Schéma pour mettre à jour des frais"""
    status: Optional[str] = None
    paid_amount: Optional[float] = None
    paid_date: Optional[datetime] = None


class FeeResponse(BaseModel):
    """Schéma pour la réponse de frais"""
    id: int
    student_id: int
    fee_type: str
    amount: float
    paid_amount: float = 0
    status: str
    due_date: datetime
    paid_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudentFilter(BaseModel):
    """Schéma pour filtrer les étudiants"""
    class_id: Optional[int] = None
    status: Optional[str] = None
    search: Optional[str] = None
