from pydantic import BaseModel
from typing import Optional
from app.schemas.employee import EmployeeResponse


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    manager_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None


class DepartmentResponse(DepartmentBase):
    id: int
    manager: Optional[EmployeeResponse] = None

    class Config:
        orm_mode = True