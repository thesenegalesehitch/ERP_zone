from pydantic import BaseModel
from datetime import datetime

class InvoiceBase(BaseModel):
    invoice_number: str
    client_id: int | None = None
    total_amount: float
    status: str = "draft"
    due_date: datetime | None = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    status: str | None = None
    due_date: datetime | None = None
    total_amount: float | None = None

class InvoiceResponse(InvoiceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
