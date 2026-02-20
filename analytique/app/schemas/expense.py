from pydantic import BaseModel
from datetime import datetime

class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: str | None = None
    notes: str | None = None

class ExpenseCreate(ExpenseBase):
    date: datetime | None = None

class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    category: str | None = None
    notes: str | None = None

class ExpenseResponse(ExpenseBase):
    id: int
    date: datetime
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
