from pydantic import BaseModel
from datetime import datetime

class ContractBase(BaseModel):
    title: str
    client_id: int | None = None
    start_date: datetime
    end_date: datetime | None = None
    value: float | None = None
    status: str = "active"

class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    title: str | None = None
    end_date: datetime | None = None
    value: float | None = None
    status: str | None = None

class ContractResponse(ContractBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
