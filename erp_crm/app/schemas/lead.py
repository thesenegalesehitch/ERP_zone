from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: str = "new"


class LeadCreate(LeadBase):
    pass


class LeadResponse(LeadBase):
    id: int
    
    class Config:
        orm_mode = True
