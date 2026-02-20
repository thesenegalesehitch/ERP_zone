from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime
from app.core.database import Base

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    value = Column(Float, nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
