from pydantic import BaseModel
from datetime import datetime

class DashboardBase(BaseModel):
    name: str
    data: dict

class DashboardCreate(DashboardBase):
    pass

class DashboardResponse(DashboardBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
