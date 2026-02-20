from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.schemas.user import UserResponse
from app.schemas.department import DepartmentResponse


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    hire_date: date
    position: Optional[str] = None
    salary: Optional[int] = None
    department_id: int


class EmployeeCreate(EmployeeBase):
    user_id: int


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    hire_date: Optional[date] = None
    position: Optional[str] = None
    salary: Optional[int] = None
    department_id: Optional[int] = None


class EmployeeResponse(EmployeeBase):
    id: int
    user: UserResponse
    department: DepartmentResponse

    class Config:
        orm_mode = True