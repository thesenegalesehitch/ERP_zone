from pydantic import BaseModel
from datetime import datetime

class CurrencyBase(BaseModel):
    code: str
    name: str
    symbol: str
    exchange_rate: float = 1.0

class CurrencyCreate(CurrencyBase):
    pass

class CurrencyUpdate(BaseModel):
    name: str | None = None
    symbol: str | None = None
    exchange_rate: float | None = None
    is_default: int | None = None

class CurrencyResponse(CurrencyBase):
    id: int
    is_default: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
