from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
import enum
from datetime import datetime
from app.core.database import Base

class QuoteStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, index=True)
    quote_number = Column(String(50), unique=True, nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(QuoteStatus), default=QuoteStatus.DRAFT)
    valid_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
