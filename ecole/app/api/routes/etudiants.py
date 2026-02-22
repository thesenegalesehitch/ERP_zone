"""
API Routes pour les étudiants

Ce module définit les routes API pour la gestion des étudiants.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/etudiants", tags=["etudiants"])


# Mock data pour les tests
MOCK_STUDENTS = [
    {
        "id": 1,
        "first_name": "Moussa",
        "last_name": "Sarr",
        "email": "moussa.sarr@ecole.sn",
        "phone": "+221771234567",
        "birth_date": datetime(2010, 5, 15),
        "class_id": 1,
        "parent_name": "M. Sarr",
        "parent_phone": "+221771234568",
        "status": "inscrit",
        "enrollment_date": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_students(
    class_id: int = None,
    status: str = None,
    search: str = None
):
    """Récupère la liste des étudiants"""
    students = MOCK_STUDENTS
    
    if class_id:
        students = [s for s in students if s["class_id"] == class_id]
    if status:
        students = [s for s in students if s["status"] == status]
    if search:
        students = [s for s in students if search.lower() in f"{s['first_name']} {s['last_name']}".lower()]
    
    return {"students": students, "total": len(students)}


@router.get("/{student_id}")
async def get_student(student_id: int):
    """Récupère un étudiant par son ID"""
    for student in MOCK_STUDENTS:
        if student["id"] == student_id:
            return student
    
    raise HTTPException(status_code=404, detail="Étudiant non trouvé")


@router.post("/")
async def create_student(student_data: dict):
    """Crée un nouvel étudiant"""
    new_student = {
        "id": len(MOCK_STUDENTS) + 1,
        **student_data,
        "status": "inscrit",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_STUDENTS.append(new_student)
    return new_student


@router.put("/{student_id}")
async def update_student(student_id: int, student_data: dict):
    """Met à jour un étudiant"""
    for i, student in enumerate(MOCK_STUDENTS):
        if student["id"] == student_id:
            MOCK_STUDENTS[i] = {
                **student,
                **student_data,
                "updated_at": datetime.now()
            }
            return MOCK_STUDENTS[i]
    
    raise HTTPException(status_code=404, detail="Étudiant non trouvé")


@router.get("/{student_id}/notes")
async def get_student_grades(student_id: int):
    """Récupère les notes d'un étudiant"""
    return {"grades": [], "total": 0}


@router.post("/{student_id}/notes")
async def create_grade(student_id: int, grade_data: dict):
    """Crée une note"""
    return {
        "id": 1,
        "student_id": student_id,
        **grade_data,
        "created_at": datetime.now()
    }


@router.get("/{student_id}/presence")
async def get_student_attendance(student_id: int):
    """Récupère la présence d'un étudiant"""
    return {"attendance": [], "total": 0}


@router.get("/{student_id}/frais")
async def get_student_fees(student_id: int):
    """Récupère les frais d'un étudiant"""
    return {"fees": [], "total": 0}


# Routes pour les classes
MOCK_CLASSES = [
    {"id": 1, "name": "CM1", "level": "primaire", "capacity": 30}
]


@router.get("/classes/")
async def get_classes():
    """Récupère la liste des classes"""
    return {"classes": MOCK_CLASSES, "total": len(MOCK_CLASSES)}


@router.post("/classes/")
async def create_class(class_data: dict):
    """Crée une classe"""
    new_class = {
        "id": len(MOCK_CLASSES) + 1,
        **class_data
    }
    MOCK_CLASSES.append(new_class)
    return new_class


# Routes pour les cours
MOCK_COURSES = []


@router.get("/cours/")
async def get_courses(class_id: int = None):
    """Récupère la liste des cours"""
    courses = MOCK_COURSES
    
    if class_id:
        courses = [c for c in courses if c.get("class_id") == class_id]
    
    return {"courses": courses, "total": len(courses)}


@router.post("/cours/")
async def create_course(course_data: dict):
    """Crée un cours"""
    new_course = {
        "id": len(MOCK_COURSES) + 1,
        **course_data,
        "created_at": datetime.now()
    }
    MOCK_COURSES.append(new_course)
    return new_course
