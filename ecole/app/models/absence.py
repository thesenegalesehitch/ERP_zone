"""
Modèle de données pour les absences

Ce module définit le modèle de données pour les absences
dans le module école.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class AbsenceModel:
    """Modèle d'absence"""
    
    def __init__(
        self,
        id: int,
        student_id: int,
        course_id: Optional[int] = None,
        date: date,
        reason: Optional[str] = None,
        status: str = "non_justifie",
        justified_by: Optional[int] = None,
        justified_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        recorded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.date = date
        self.reason = reason
        self.status = status
        self.justified_by = justified_by
        self.justified_at = justified_at
        self.notes = notes
        self.recorded_by = recorded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "date": self.date,
            "reason": self.reason,
            "status": self.status,
            "justified_by": self.justified_by,
            "justified_at": self.justified_at,
            "notes": self.notes,
            "recorded_by": self.recorded_by,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AbsenceModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            student_id=data.get("student_id"),
            course_id=data.get("course_id"),
            date=data.get("date"),
            reason=data.get("reason"),
            status=data.get("status", "non_justifie"),
            justified_by=data.get("justified_by"),
            justified_at=data.get("justified_at"),
            notes=data.get("notes"),
            recorded_by=data.get("recorded_by"),
            created_at=data.get("created_at")
        )
    
    def is_justified(self) -> bool:
        """Vérifie si l'absence est justifiée"""
        return self.status == "justifie"


class ScheduleModel:
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
        semester: str,
        academic_year: str,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
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
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
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
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @staticmethod
    def get_day_name(day: int) -> str:
        """Retourne le nom du jour"""
        days = {
            1: "Lundi",
            2: "Mardi",
            3: "Mercredi",
            4: "Jeudi",
            5: "Vendredi",
            6: "Samedi",
            0: "Dimanche"
        }
        return days.get(day, "Inconnu")


class ExamModel:
    """Modèle d'examen"""
    
    def __init__(
        self,
        id: int,
        course_id: int,
        exam_type: str,
        exam_date: date,
        start_time: str,
        end_time: str,
        room: Optional[str] = None,
        semester: str,
        academic_year: str,
        total_marks: float = 100,
        passing_marks: float = 50,
        is_active: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.course_id = course_id
        self.exam_type = exam_type
        self.exam_date = exam_date
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
        self.semester = semester
        self.academic_year = academic_year
        self.total_marks = total_marks
        self.passing_marks = passing_marks
        self.is_active = is_active
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "course_id": self.course_id,
            "exam_type": self.exam_type,
            "exam_date": self.exam_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "room": self.room,
            "semester": self.semester,
            "academic_year": self.academic_year,
            "total_marks": self.total_marks,
            "passing_marks": self.passing_marks,
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_passing(self, marks: float) -> bool:
        """Vérifie si la note est suffisante"""
        return marks >= self.passing_marks


class ExamResultModel:
    """Modèle de résultat d'examen"""
    
    def __init__(
        self,
        id: int,
        exam_id: int,
        student_id: int,
        marks_obtained: float,
        grade: Optional[str] = None,
        remarks: Optional[str] = None,
        graded_by: int = None,
        graded_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.exam_id = exam_id
        self.student_id = student_id
        self.marks_obtained = marks_obtained
        self.grade = grade
        self.remarks = remarks
        self.graded_by = graded_by
        self.graded_at = graded_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "exam_id": self.exam_id,
            "student_id": self.student_id,
            "marks_obtained": self.marks_obtained,
            "grade": self.grade,
            "remarks": self.remarks,
            "graded_by": self.graded_by,
            "graded_at": self.graded_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
