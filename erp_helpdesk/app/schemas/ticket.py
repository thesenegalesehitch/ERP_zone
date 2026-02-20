from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.ticket import TicketStatus, TicketPriority


class TicketCommentBase(BaseModel):
    content: str


class TicketCommentCreate(TicketCommentBase):
    pass


class TicketCommentResponse(TicketCommentBase):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TicketBase(BaseModel):
    title: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_to_id: Optional[int] = None


class TicketResponse(TicketBase):
    id: int
    status: TicketStatus
    requester_id: int
    assigned_to_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    comments: List[TicketCommentResponse] = []

    class Config:
        from_attributes = True
