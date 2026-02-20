from pydantic import BaseModel
from typing import Optional
from datetime import date


class InvoiceBase(BaseModel):
    invoice_number: str
    client_name: str
    amount: float
    date: date
    status: str = "pending"


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    invoice_number: Optional[str] = None
    client_name: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[date] = None
    status: Optional[str] = None


class InvoiceResponse(InvoiceBase):
    id: int
    
    class Config:
        orm_mode = True
