from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    report_type = Column(String)  # sales, inventory, financial
    data = Column(String)  # JSON data
