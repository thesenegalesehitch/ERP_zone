from pydantic import BaseModel
from datetime import datetime

class ActivityLogBase(BaseModel):
    action: str
    entity_type: str | None = None
    entity_id: int | None = None
    details: str | None = None
    ip_address: str | None = None

class ActivityLogCreate(ActivityLogBase):
    user_id: int | None = None

class ActivityLogResponse(ActivityLogBase):
    id: int
    user_id: int | None
    created_at: datetime
    class Config:
        from_attributes = True
