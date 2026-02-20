from pydantic import BaseModel
from typing import Optional
from datetime import date


class PaymentBase(BaseModel):
    amount: float
    date: date
    method: Optional[str] = None
    reference: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    date: Optional[date] = None
    method: Optional[str] = None
    reference: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: int
    
    class Config:
        orm_mode = True
