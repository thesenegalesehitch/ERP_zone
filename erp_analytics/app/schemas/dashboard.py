from pydantic import BaseModel
from typing import Optional


class DashboardBase(BaseModel):
    name: str
    config: Optional[str] = None


class DashboardCreate(DashboardBase):
    pass


class DashboardResponse(DashboardBase):
    id: int
    
    class Config:
        orm_mode = True
