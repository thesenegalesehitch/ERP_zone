from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from datetime import datetime
from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(500), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
