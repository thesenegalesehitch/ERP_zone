from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum as PyEnum


class MovementType(PyEnum):
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"


class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    quantity = Column(Integer, nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String)
    
    product = relationship("Product", back_populates="movements")
    supplier = relationship("Supplier", back_populates="stock_movements")
