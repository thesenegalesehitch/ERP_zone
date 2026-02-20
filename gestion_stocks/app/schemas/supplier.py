from pydantic import BaseModel, EmailStr
from typing import Optional


class SupplierBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SupplierResponse(SupplierBase):
    id: int
    
    class Config:
        orm_mode = True
