from pydantic import BaseModel
from typing import Optional
from datetime import date


class TransactionBase(BaseModel):
    description: Optional[str] = None
    amount: float
    date: date
    account_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[date] = None
    account_id: Optional[int] = None


class TransactionResponse(TransactionBase):
    id: int
    
    class Config:
        orm_mode = True
