from pydantic import BaseModel
from datetime import datetime

class OrderBase(BaseModel):
    order_number: str
    customer_id: int | None = None
    total_amount: float
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: str | None = None
    total_amount: float | None = None

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
