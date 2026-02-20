from sqlalchemy import Column, Integer, String
from app.core.database import Base


class BillOfMaterials(Base):
    __tablename__ = "bills_of_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False, index=True)
    material_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
