"""
Modèle de données pour les cours

Ce module définit le modèle de données pour les cours
dans le module de gestion de l'école.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class CourseModel:
    """Modèle de cours"""
    
    def __init__(
        self,
        id: int,
        course_code: str,
        name: str,
        description: Optional[str] = None,
        credits: int = 0,
        hours: float = 0,
        course_type: str = "magistral",
        level: Optional[str] = None,
        department: Optional[str] = None,
        teacher_id: Optional[int] = None,
        is_active: bool = True,
        prerequisites: Optional[str] = None,
        objectives: Optional[str] = None,
        syllabus: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.course_code = course_code
        self.name = name
        self.description = description
        self.credits = credits
        self.hours = hours
        self.course_type = course_type
        self.level = level
        self.department = department
        self.teacher_id = teacher_id
        self.is_active = is_active
        self.prerequisites = prerequisites
        self.objectives = objectives
        self.syllabus = syllabus
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "course_code": self.course_code,
            "name": self.name,
            "description": self.description,
            "credits": self.credits,
            "hours": self.hours,
            "course_type": self.course_type,
            "level": self.level,
            "department": self.department,
            "teacher_id": self.teacher_id,
            "is_active": self.is_active,
            "prerequisites": self.prerequisites,
            "objectives": self.objectives,
            "syllabus": self.syllabus,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CourseModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            course_code=data.get("course_code"),
            name=data.get("name"),
            description=data.get("description"),
            credits=data.get("credits", 0),
            hours=data.get("hours", 0),
            course_type=data.get("course_type", "magistral"),
            level=data.get("level"),
            department=data.get("department"),
            teacher_id=data.get("teacher_id"),
            is_active=data.get("is_active", True),
            prerequisites=data.get("prerequisites"),
            objectives=data.get("objectives"),
            syllabus=data.get("syllabus"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active_status(self) -> bool:
        """Vérifie si actif"""
        return self.is_active


class CourseScheduleModel:
    """Modèle d'emploi du temps"""
    
    def __init__(
        self,
        id: int,
        course_id: int,
        day_of_week: int,
        start_time: str,
        end_time: str,
        room: Optional[str] = None,
        building: Optional[str] = None,
        semester: str = "S1",
        academic_year: str = "2023-2024",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.course_id = course_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
        self.building = building
        self.semester = semester
        self.academic_year = academic_year
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "course_id": self.course_id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "room": self.room,
            "building": self.building,
            "semester": self.semester,
            "academic_year": self.academic_year,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def duration_hours(self) -> float:
        """Durée en heures"""
        try:
            start = datetime.strptime(self.start_time, "%H:%M")
            end = datetime.strptime(self.end_time, "%H:%M")
            delta = end - start
            return delta.seconds / 3600
        except:
            return 0


class CourseMaterialModel:
    """Modèle de matériel de cours"""
    
    def __init__(
        self,
        id: int,
        course_id: int,
        title: str,
        material_type: str = "document",
        file_path: Optional[str] = None,
        url: Optional[str] = None,
        description: Optional[str] = None,
        uploaded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.course_id = course_id
        self.title = title
        self.material_type = material_type
        self.file_path = file_path
        self.url = url
        self.description = description
        self.uploaded_by = uploaded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "material_type": self.material_type,
            "file_path": self.file_path,
            "url": self.url,
            "description": self.description,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at
        }
