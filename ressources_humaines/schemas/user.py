from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.role import RoleResponse


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role_id: int


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: RoleResponse

    class Config:
        orm_mode = True