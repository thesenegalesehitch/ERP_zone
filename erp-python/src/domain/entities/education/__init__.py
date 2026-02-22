"""
Education Entity for ERP System.

This module provides entities for education/school management
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class EnrollmentStatus(str, Enum):
    """Enrollment status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    GRADUATED = "graduated"
    SUSPENDED = "suspended"
    WITHDRAWN = "withdrawn"
    DROPPED = "dropped"


class AttendanceStatus(str, Enum):
    """Attendance status enumeration."""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"


class GradeStatus(str, Enum):
    """Grade status enumeration."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PUBLISHED = "published"


@dataclass(frozen=True)
class CourseGrade:
    """
    Value Object representing a course grade.
    Immutable and validated.
    """
    id: str
    student_id: str
    student_name: str
    course_id: str
    course_name: str
    grade: Decimal
    letter_grade: str
    status: GradeStatus
    remarks: str = ""
    graded_by: str = ""
    graded_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student_name,
            "course_id": self.course_id,
            "course_name": self.course_name,
            "grade": str(self.grade),
            "letter_grade": self.letter_grade,
            "status": self.status.value,
            "remarks": self.remarks,
            "graded_by": self.graded_by,
            "graded_at": self.graded_at.isoformat() if self.graded_at else None
        }


@dataclass(frozen=True)
class AttendanceRecord:
    """
    Value Object representing an attendance record.
    Immutable and validated.
    """
    id: str
    student_id: str
    student_name: str
    course_id: str
    course_name: str
    date: date
    status: AttendanceStatus
    remarks: str = ""
    recorded_by: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student_name,
            "course_id": self.course_id,
            "course_name": self.course_name,
            "date": self.date.isoformat(),
            "status": self.status.value,
            "remarks": self.remarks,
            "recorded_by": self.recorded_by
        }


@dataclass(frozen=True)
class Student:
    """
    Student entity for managing students.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        student_number: Student number
        first_name: First name
        last_name: Last name
        date_of_birth: Date of birth
        gender: Gender
        email: Email address
        phone: Phone number
        address: Address
        enrollment_status: Current enrollment status
        enrollment_date: Enrollment date
        program_id: Program ID
        program_name: Program name
        year_level: Current year level
        gpa: Grade Point Average
        grades: List of grades
        attendance: Attendance records
        guardian_name: Guardian name
        guardian_phone: Guardian phone
        guardian_email: Guardian email
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    student_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    email: str
    phone: str
    address: str
    enrollment_status: EnrollmentStatus
    enrollment_date: date
    program_id: str
    program_name: str
    year_level: int = 1
    gpa: Decimal = field(default=Decimal("0"))
    grades: List[CourseGrade] = field(default_factory=list)
    attendance: List[AttendanceRecord] = field(default_factory=list)
    guardian_name: str = ""
    guardian_phone: str = ""
    guardian_email: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.student_number:
            raise ValueError("student_number cannot be empty")
        if not self.first_name or not self.last_name:
            raise ValueError("first_name and last_name cannot be empty")
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self) -> bool:
        return self.enrollment_status == EnrollmentStatus.ACTIVE
    
    @property
    def is_enrolled(self) -> bool:
        return self.enrollment_status in [EnrollmentStatus.ACTIVE, EnrollmentStatus.PENDING]
    
    @property
    def total_credits(self) -> int:
        return len(self.grades)
    
    @property
    def attendance_percentage(self) -> float:
        if not self.attendance:
            return 100.0
        present = sum(1 for a in self.attendance if a.status == AttendanceStatus.PRESENT)
        return (present / len(self.attendance)) * 100
    
    def calculate_gpa(self) -> None:
        """Calculate GPA from grades."""
        if not self.grades:
            self.gpa = Decimal("0")
            return
        
        total = sum(g.grade for g in self.grades)
        self.gpa = total / len(self.grades)
    
    def add_grade(self, grade: CourseGrade) -> None:
        """Add a grade."""
        self.grades.append(grade)
        self.calculate_gpa()
    
    def record_attendance(self, record: AttendanceRecord) -> None:
        """Record attendance."""
        self.attendance.append(record)
    
    def enroll(self, program_id: str, program_name: str, year: int) -> None:
        """Enroll in a program."""
        self.enrollment_status = EnrollmentStatus.ACTIVE
        self.program_id = program_id
        self.program_name = program_name
        self.year_level = year
        self.enrollment_date = date.today()
    
    def graduate(self) -> None:
        """Mark as graduated."""
        self.enrollment_status = EnrollmentStatus.GRADUATED
    
    def withdraw(self, reason: str) -> None:
        """Withdraw from program."""
        self.enrollment_status = EnrollmentStatus.WITHDRAWN
        self.metadata["withdrawal_reason"] = reason
    
    def suspend(self, reason: str) -> None:
        """Suspend the student."""
        self.enrollment_status = EnrollmentStatus.SUSPENDED
        self.metadata["suspension_reason"] = reason
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "student_number": self.student_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.isoformat(),
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "enrollment_status": self.enrollment_status.value,
            "enrollment_date": self.enrollment_date.isoformat(),
            "program_id": self.program_id,
            "program_name": self.program_name,
            "year_level": self.year_level,
            "gpa": str(self.gpa),
            "grades": [g.to_dict() for g in self.grades],
            "attendance": [a.to_dict() for a in self.attendance],
            "guardian_name": self.guardian_name,
            "guardian_phone": self.guardian_phone,
            "guardian_email": self.guardian_email,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "is_enrolled": self.is_enrolled,
            "total_credits": self.total_credits,
            "attendance_percentage": self.attendance_percentage
        }


class StudentBuilder:
    """Builder for creating Student instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._student_number: Optional[str] = None
        self._first_name: Optional[str] = None
        self._last_name: Optional[str] = None
        self._date_of_birth: Optional[date] = None
        self._gender: str = ""
        self._email: str = ""
        self._phone: str = ""
        self._address: str = ""
        self._enrollment_status: EnrollmentStatus = EnrollmentStatus.PENDING
        self._enrollment_date: Optional[date] = None
        self._program_id: str = ""
        self._program_name: str = ""
        self._year_level: int = 1
        self._gpa: Decimal = Decimal("0")
        self._grades: List[CourseGrade] = []
        self._attendance: List[AttendanceRecord] = []
        self._guardian_name: str = ""
        self._guardian_phone: str = ""
        self._guardian_email: str = ""
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, student_id: str) -> "StudentBuilder":
        self._id = student_id
        return self
    
    def with_student_number(self, student_number: str) -> "StudentBuilder":
        self._student_number = student_number
        return self
    
    def with_name(self, first_name: str, last_name: str) -> "StudentBuilder":
        self._first_name = first_name
        self._last_name = last_name
        return self
    
    def with_personal_info(self, dob: date, gender: str, email: str, phone: str) -> "StudentBuilder":
        self._date_of_birth = dob
        self._gender = gender
        self._email = email
        self._phone = phone
        return self
    
    def with_address(self, address: str) -> "StudentBuilder":
        self._address = address
        return self
    
    def with_enrollment(self, status: EnrollmentStatus, program_id: str, program_name: str, year: int) -> "StudentBuilder":
        self._enrollment_status = status
        self._program_id = program_id
        self._program_name = program_name
        self._year_level = year
        return self
    
    def with_grades(self, grades: List[CourseGrade]) -> "StudentBuilder":
        self._grades = grades
        return self
    
    def with_attendance(self, attendance: List[AttendanceRecord]) -> "StudentBuilder":
        self._attendance = attendance
        return self
    
    def with_guardian(self, name: str, phone: str, email: str) -> "StudentBuilder":
        self._guardian_name = name
        self._guardian_phone = phone
        self._guardian_email = email
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "StudentBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Student:
        if not self._id:
            self._id = str(uuid4())
        if not self._student_number:
            self._student_number = f"STU-{str(self._id)[:8]}"
        if not self._first_name or not self._last_name:
            raise ValueError("first_name and last_name are required")
        
        student = Student(
            id=self._id,
            student_number=self._student_number,
            first_name=self._first_name,
            last_name=self._last_name,
            date_of_birth=self._date_of_birth or date(2000, 1, 1),
            gender=self._gender,
            email=self._email,
            phone=self._phone,
            address=self._address,
            enrollment_status=self._enrollment_status,
            enrollment_date=self._enrollment_date or date.today(),
            program_id=self._program_id,
            program_name=self._program_name,
            year_level=self._year_level,
            gpa=self._gpa,
            grades=self._grades,
            attendance=self._attendance,
            guardian_name=self._guardian_name,
            guardian_phone=self._guardian_phone,
            guardian_email=self._guardian_email,
            metadata=self._metadata
        )
        
        student.calculate_gpa()
        return student


def create_student(
    first_name: str,
    last_name: str,
    date_of_birth: date,
    **kwargs
) -> Student:
    """Factory function to create a student."""
    builder = StudentBuilder()
    builder.with_name(first_name, last_name)
    builder.with_personal_info(date_of_birth, kwargs.get("gender", ""), kwargs.get("email", ""), kwargs.get("phone", ""))
    
    if student_number := kwargs.get("student_number"):
        builder.with_student_number(student_number)
    if address := kwargs.get("address"):
        builder.with_address(address)
    if enrollment_status := kwargs.get("enrollment_status"):
        program_id = kwargs.get("program_id", "")
        program_name = kwargs.get("program_name", "")
        year = kwargs.get("year_level", 1)
        builder.with_enrollment(enrollment_status, program_id, program_name, year)
    if guardian_name := kwargs.get("guardian_name"):
        guardian_phone = kwargs.get("guardian_phone", "")
        guardian_email = kwargs.get("guardian_email", "")
        builder.with_guardian(guardian_name, guardian_phone, guardian_email)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_course_grade(
    student_id: str,
    student_name: str,
    course_id: str,
    course_name: str,
    grade: Decimal,
    **kwargs
) -> CourseGrade:
    """Factory function to create a course grade."""
    letter = "F"
    if grade >= Decimal("90"):
        letter = "A"
    elif grade >= Decimal("80"):
        letter = "B"
    elif grade >= Decimal("70"):
        letter = "C"
    elif grade >= Decimal("60"):
        letter = "D"
    
    return CourseGrade(
        id=str(uuid4()),
        student_id=student_id,
        student_name=student_name,
        course_id=course_id,
        course_name=course_name,
        grade=grade,
        letter_grade=letter,
        status=kwargs.get("status", GradeStatus.SUBMITTED),
        remarks=kwargs.get("remarks", ""),
        graded_by=kwargs.get("graded_by", "")
    )


def create_attendance_record(
    student_id: str,
    student_name: str,
    course_id: str,
    course_name: str,
    date: date,
    status: AttendanceStatus,
    **kwargs
) -> AttendanceRecord:
    """Factory function to create an attendance record."""
    return AttendanceRecord(
        id=str(uuid4()),
        student_id=student_id,
        student_name=student_name,
        course_id=course_id,
        course_name=course_name,
        date=date,
        status=status,
        remarks=kwargs.get("remarks", ""),
        recorded_by=kwargs.get("recorded_by", "")
    )
