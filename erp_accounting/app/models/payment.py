from sqlalchemy import Column, Integer, String, Float, Date
from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    method = Column(String)  # cash, card, transfer
    reference = Column(String)
