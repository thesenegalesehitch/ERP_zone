from pydantic import BaseModel
from datetime import datetime

class TaxBase(BaseModel):
    name: str
    rate: float
    description: str | None = None

class TaxCreate(TaxBase):
    pass

class TaxUpdate(BaseModel):
    name: str | None = None
    rate: float | None = None
    description: str | None = None
    is_active: int | None = None

class TaxResponse(TaxBase):
    id: int
    is_active: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
