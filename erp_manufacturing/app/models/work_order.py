from sqlalchemy import Column, Integer, String
from app.core.database import Base


class WorkOrder(Base):
    __tablename__ = "work_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="pending")  # pending, in_progress, completed
