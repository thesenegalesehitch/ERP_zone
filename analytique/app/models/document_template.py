from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
import enum
from datetime import datetime
from app.core.database import Base

class TemplateType(str, enum.Enum):
    INVOICE = "invoice"
    QUOTE = "quote"
    ORDER = "order"
    RECEIPT = "receipt"
    EMAIL = "email"

class DocumentTemplate(Base):
    __tablename__ = "document_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    template_type = Column(Enum(TemplateType), nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
