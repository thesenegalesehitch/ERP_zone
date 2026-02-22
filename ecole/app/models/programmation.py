"""
Modèle de données pour la programmation des cours

Ce module définit le modèle de données pour la programmation
dans le module de gestion de l'école.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date, time
from typing import Optional


class ScheduleModel:
    """Modèle de programmation"""
    
    def __init__(
        self,
        id: int,
        course_id: int,
        teacher_id: int,
        room_id: Optional[int] = None,
        group_id: Optional[int] = None,
        day_of_week: int = 1,
        start_time: time = None,
        end_time: time = None,
        semester: str = "S1",
        academic_year: str = "2023-2024",
        is_cancelled: bool = False,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.room_id = room_id
        self.group_id = group_id
        self.day_of_week = day_of_week
        self.start_time = start_time or time(8, 0)
        self.end_time = end_time or time(10, 0)
        self.semester = semester
        self.academic_year = academic_year
        self.is_cancelled = is_cancelled
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "course_id": self.course_id,
            "teacher_id": self.teacher_id,
            "room_id": self.room_id,
            "group_id": self.group_id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "semester": self.semester,
            "academic_year": self.academic_year,
            "is_cancelled": self.is_cancelled,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ScheduleModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            course_id=data.get("course_id"),
            teacher_id=data.get("teacher_id"),
            room_id=data.get("room_id"),
            group_id=data.get("group_id"),
            day_of_week=data.get("day_of_week", 1),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            semester=data.get("semester", "S1"),
            academic_year=data.get("academic_year", "2023-2024"),
            is_cancelled=data.get("is_cancelled", False),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def duration_minutes(self) -> int:
        """Durée en minutes"""
        if not self.start_time or not self.end_time:
            return 0
        from datetime import datetime, timedelta
        start = datetime.combine(date.today(), self.start_time)
        end = datetime.combine(date.today(), self.end_time)
        delta = end - start
        return int(delta.total_seconds() / 60)
    
    def is_cancelled_status(self) -> bool:
        """Vérifie si annulé"""
        return self.is_cancelled


class RoomModel:
    """Modèle de salle"""
    
    def __init__(
        self,
        id: int,
        name: str,
        building: Optional[str] = None,
        floor: Optional[int] = None,
        capacity: int = 30,
        room_type: str = "cours",
        has_projector: bool = False,
        has_computer: bool = False,
        is_available: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.building = building
        self.floor = floor
        self.capacity = capacity
        self.room_type = room_type
        self.has_projector = has_projector
        self.has_computer = has_computer
        self.is_available = is_available
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "building": self.building,
            "floor": self.floor,
            "capacity": self.capacity,
            "room_type": self.room_type,
            "has_projector": self.has_projector,
            "has_computer": self.has_computer,
            "is_available": self.is_available,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_available_status(self) -> bool:
        """Vérifie si disponible"""
        return self.is_available


class GroupModel:
    """Modèle de groupe"""
    
    def __init__(
        self,
        id: int,
        name: str,
        academic_year: str,
        semester: str = "S1",
        level: Optional[str] = None,
        department: Optional[str] = None,
        capacity: int = 30,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.academic_year = academic_year
        self.semester = semester
        self.level = level
        self.department = department
        self.capacity = capacity
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "academic_year": self.academic_year,
            "semester": self.semester,
            "level": self.level,
            "department": self.department,
            "capacity": self.capacity,
            "notes": self.notes,
            "created_at": self.created_at
        }
