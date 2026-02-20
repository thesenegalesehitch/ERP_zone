from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    location = Column(String)
    capacity = Column(Integer)
