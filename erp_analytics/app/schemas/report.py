from pydantic import BaseModel
from typing import Optional


class ReportBase(BaseModel):
    name: str
    report_type: Optional[str] = None
    data: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportResponse(ReportBase):
    id: int
    
    class Config:
        orm_mode = True
