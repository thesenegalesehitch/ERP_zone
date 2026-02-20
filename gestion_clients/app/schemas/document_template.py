from pydantic import BaseModel
from datetime import datetime

class DocumentTemplateBase(BaseModel):
    name: str
    template_type: str
    content: str

class DocumentTemplateCreate(DocumentTemplateBase):
    pass

class DocumentTemplateUpdate(BaseModel):
    name: str | None = None
    content: str | None = None
    is_active: int | None = None

class DocumentTemplateResponse(DocumentTemplateBase):
    id: int
    is_active: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
