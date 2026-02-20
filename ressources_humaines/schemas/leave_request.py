from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.schemas.employee import EmployeeResponse
from app.models.leave_request import LeaveStatus


class LeaveRequestBase(BaseModel):
    start_date: date
    end_date: date
    reason: str


class LeaveRequestCreate(LeaveRequestBase):
    pass


class LeaveRequestUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None
    status: Optional[LeaveStatus] = None


class LeaveRequestResponse(LeaveRequestBase):
    id: int
    status: LeaveStatus
    employee: EmployeeResponse

    class Config:
        orm_mode = True