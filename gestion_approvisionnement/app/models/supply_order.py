from sqlalchemy import Column, Integer, String
from app.core.database import Base


class SupplyOrder(Base):
    __tablename__ = "supply_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    supplier = Column(String)
    status = Column(String, default="pending")  # pending, ordered, delivered
