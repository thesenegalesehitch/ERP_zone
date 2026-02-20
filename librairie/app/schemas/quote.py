from pydantic import BaseModel
from datetime import datetime

class QuoteBase(BaseModel):
    quote_number: str
    client_id: int | None = None
    total_amount: float
    status: str = "draft"
    valid_until: datetime | None = None

class QuoteCreate(QuoteBase):
    pass

class QuoteUpdate(BaseModel):
    status: str | None = None
    valid_until: datetime | None = None
    total_amount: float | None = None

class QuoteResponse(QuoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
