from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    payment_method = Column(String)
