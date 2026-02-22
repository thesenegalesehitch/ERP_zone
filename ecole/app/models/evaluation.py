"""
Modèle de données pour les évaluations

Ce module définit le modèle de données pour les évaluations
dans le module de gestion de l'école.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class EvaluationModel:
    """Modèle d'évaluation"""
    
    def __init__(
        self,
        id: int,
        title: str,
        course_id: int,
        evaluation_type: str = "examen",
        description: Optional[str] = None,
        date: date = None,
        duration_minutes: int = 60,
        total_score: float = 20,
        passing_score: float = 10,
        semester: str = "S1",
        academic_year: str = "2023-2024",
        is_published: bool = False,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.course_id = course_id
        self.evaluation_type = evaluation_type
        self.description = description
        self.date = date or date.today()
        self.duration_minutes = duration_minutes
        self.total_score = total_score
        self.passing_score = passing_score
        self.semester = semester
        self.academic_year = academic_year
        self.is_published = is_published
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "title": self.title,
            "course_id": self.course_id,
            "evaluation_type": self.evaluation_type,
            "description": self.description,
            "date": self.date,
            "duration_minutes": self.duration_minutes,
            "total_score": self.total_score,
            "passing_score": self.passing_score,
            "semester": self.semester,
            "academic_year": self.academic_year,
            "is_published": self.is_published,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EvaluationModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            title=data.get("title"),
            course_id=data.get("course_id"),
            evaluation_type=data.get("evaluation_type", "examen"),
            description=data.get("description"),
            date=data.get("date"),
            duration_minutes=data.get("duration_minutes", 60),
            total_score=data.get("total_score", 20),
            passing_score=data.get("passing_score", 10),
            semester=data.get("semester", "S1"),
            academic_year=data.get("academic_year", "2023-2024"),
            is_published=data.get("is_published", False),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_published_status(self) -> bool:
        """Vérifie si publiée"""
        return self.is_published


class GradeModel:
    """Modèle de note"""
    
    def __init__(
        self,
        id: int,
        student_id: int,
        evaluation_id: int,
        score: float = 0,
        grade: Optional[str] = None,
        comments: Optional[str] = None,
        graded_by: int = None,
        graded_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.student_id = student_id
        self.evaluation_id = evaluation_id
        self.score = score
        self.grade = grade
        self.comments = comments
        self.graded_by = graded_by
        self.graded_at = graded_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "evaluation_id": self.evaluation_id,
            "score": self.score,
            "grade": self.grade,
            "comments": self.comments,
            "graded_by": self.graded_by,
            "graded_at": self.graded_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_grade(self, total_score: float = 20) -> str:
        """Calcule la lettre de grade"""
        percentage = (self.score / total_score) * 100
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"


class ExamSupervisionModel:
    """Modèle de surveillance d'examen"""
    
    def __init__(
        self,
        id: int,
        evaluation_id: int,
        teacher_id: int,
        room: str,
        capacity: int = 30,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.evaluation_id = evaluation_id
        self.teacher_id = teacher_id
        self.room = room
        self.capacity = capacity
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "evaluation_id": self.evaluation_id,
            "teacher_id": self.teacher_id,
            "room": self.room,
            "capacity": self.capacity,
            "notes": self.notes,
            "created_at": self.created_at
        }
