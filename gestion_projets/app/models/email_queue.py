from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
import enum
from datetime import datetime
from app.core.database import Base

class EmailStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class EmailQueue(Base):
    __tablename__ = "email_queue"
    id = Column(Integer, primary_key=True, index=True)
    to_email = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(Enum(EmailStatus), default=EmailStatus.PENDING)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
