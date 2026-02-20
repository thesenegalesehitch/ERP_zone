from pydantic import BaseModel
from datetime import datetime

class SettingBase(BaseModel):
    key: str
    value: str | None = None
    description: str | None = None

class SettingCreate(SettingBase):
    pass

class SettingUpdate(BaseModel):
    value: str | None = None
    description: str | None = None

class SettingResponse(SettingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
