from pydantic import BaseModel
from datetime import datetime

class PaymentBase(BaseModel):
    invoice_id: int | None = None
    amount: float
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: str | None = None
    transaction_id: str | None = None

class PaymentResponse(PaymentBase):
    id: int
    status: str
    transaction_id: str | None
    payment_date: datetime
    created_at: datetime
    class Config:
        from_attributes = True
