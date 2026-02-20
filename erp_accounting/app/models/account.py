from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    account_number = Column(String, unique=True, nullable=False)
    account_type = Column(String, nullable=False)  # asset, liability, equity, revenue, expense
    balance = Column(Float, default=0.0)
