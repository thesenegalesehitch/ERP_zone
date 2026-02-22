"""
Configuration du module ecole

Ce module contient les configurations et utilitaires
pour le module de gestion scolaire.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class StudentManager:
    """Gestionnaire d'étudiants"""
    
    @staticmethod
    def calculate_average(grades: List[float]) -> float:
        """
        Calcule la moyenne des notes.
        
        Args:
            grades: Liste des notes
        
        Returns:
            Moyenne
        """
        if not grades:
            return 0.0
        return sum(grades) / len(grades)
    
    @staticmethod
    def get_student_status(average: float) -> str:
        """
        Détermine le statut de l'étudiant.
        
        Args:
            average: Moyenne
        
        Returns:
            Statut
        """
        if average >= 16:
            return "excellent"
        elif average >= 14:
            return "bien"
        elif average >= 12:
            return "assez_bien"
        elif average >= 10:
            return "passable"
        else:
            return "insuffisant"
    
    @staticmethod
    def check_attendance_rate(
        present_days: int,
        total_days: int
    ) -> float:
        """
        Calcule le taux de présence.
        
        Args:
            present_days: Jours présents
            total_days: Total des jours
        
        Returns:
            Taux de présence
        """
        if total_days == 0:
            return 0.0
        return (present_days / total_days) * 100


class CourseManager:
    """Gestionnaire de cours"""
    
    @staticmethod
    def calculate_course_hours(
        sessions: List[Dict]
    ) -> int:
        """
        Calcule les heures de cours.
        
        Args:
            sessions: Sessions
        
        Returns:
            Nombre d'heures
        """
        total_hours = 0
        for session in sessions:
            if session.get("duration"):
                total_hours += session["duration"]
        return total_hours
    
    @staticmethod
    def get_course_schedule(
        course: Dict,
        week: int
    ) -> List[Dict]:
        """
        Génère l'emploi du temps.
        
        Args:
            course: Cours
            week: Semaine
        
        Returns:
            Schedule
        """
        schedule = []
        sessions = course.get("sessions", [])
        
        for session in sessions:
            if session.get("week") == week:
                schedule.append(session)
        
        return schedule


class GradeCalculator:
    """Calculateur de notes"""
    
    @staticmethod
    def calculate_final_grade(
        continuous_assessment: float,
        exam_grade: float,
        weight_ca: float = 0.4,
        weight_exam: float = 0.6
    ) -> float:
        """
        Calcule la note finale.
        
        Args:
            continuous_assessment: Contrôle continu
            exam_grade: Note d'examen
            weight_ca: Pondération contrôle continu
            weight_exam: Pondération examen
        
        Returns:
            Note finale
        """
        return (continuous_assessment * weight_ca) + (exam_grade * weight_exam)
    
    @staticmethod
    def get_grade_letter(grade: float) -> str:
        """
        Convertit la note en lettre.
        
        Args:
            grade: Note
        
        Returns:
            Lettre
        """
        if grade >= 18:
            return "A+"
        elif grade >= 16:
            return "A"
        elif grade >= 14:
            return "B"
        elif grade >= 12:
            return "C"
        elif grade >= 10:
            return "D"
        else:
            return "F"


class AttendanceTracker:
    """Suivi de présence"""
    
    @staticmethod
    def mark_attendance(
        student_id: int,
        course_id: int,
        date: datetime,
        status: str
    ) -> Dict:
        """
        Marque la présence.
        
        Args:
            student_id: ID étudiant
            course_id: ID cours
            date: Date
            status: Statut
        
        Returns:
            Enregistrement
        """
        return {
            "student_id": student_id,
            "course_id": course_id,
            "date": date,
            "status": status,
            "recorded_at": datetime.now()
        }
    
    @staticmethod
    def get_attendance_summary(
        records: List[Dict]
    ) -> Dict:
        """
        Résumé des présences.
        
        Args:
            records: Enregistrements
        
        Returns:
            Résumé
        """
        present = sum(1 for r in records if r.get("status") == "present")
        absent = sum(1 for r in records if r.get("status") == "absent")
        late = sum(1 for r in records if r.get("status") == "late")
        
        return {
            "present": present,
            "absent": absent,
            "late": late,
            "total": len(records),
            "attendance_rate": (present / len(records) * 100) if records else 0
        }


class ScheduleGenerator:
    """Générateur d'emploi du temps"""
    
    @staticmethod
    def generate_weekly_schedule(
        courses: List[Dict],
        available_slots: List[Dict]
    ) -> List[Dict]:
        """
        Génère l'emploi du temps hebdomadaire.
        
        Args:
            courses: Cours
            available_slots: Créneaux disponibles
        
        Returns:
            Emploi du temps
        """
        schedule = []
        
        for course in courses:
            for slot in available_slots:
                if slot.get("available"):
                    schedule.append({
                        "course_id": course.get("id"),
                        "course_name": course.get("name"),
                        "day": slot.get("day"),
                        "start_time": slot.get("start_time"),
                        "end_time": slot.get("end_time"),
                        "room": slot.get("room")
                    })
                    break
        
        return schedule


def generate_student_report(
    student: Dict,
    grades: List[Dict],
    attendance: List[Dict]
) -> Dict:
    """
    Génère un rapport d'étudiant.
    
    Args:
        student: Étudiant
        grades: Notes
        attendance: Présences
    
    Returns:
        Rapport
    """
    grade_values = [g.get("grade", 0) for g in grades]
    average = StudentManager.calculate_average(grade_values)
    status = StudentManager.get_student_status(average)
    attendance_summary = AttendanceTracker.get_attendance_summary(attendance)
    
    return {
        "student": student,
        "average": average,
        "status": status,
        "grades_count": len(grades),
        "attendance": attendance_summary,
        "generated_at": datetime.now()
    }
