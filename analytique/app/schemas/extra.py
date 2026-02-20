from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExtraBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExtraCreate(ExtraBase):
    pass

class ExtraResponse(ExtraBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
