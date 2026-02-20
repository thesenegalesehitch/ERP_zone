from pydantic import BaseModel
from datetime import datetime

class EmailQueueBase(BaseModel):
    to_email: str
    subject: str
    body: str

class EmailQueueCreate(EmailQueueBase):
    pass

class EmailQueueResponse(EmailQueueBase):
    id: int
    status: str
    error_message: str | None
    created_at: datetime
    sent_at: datetime | None
    class Config:
        from_attributes = True
