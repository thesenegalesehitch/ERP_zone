from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, default="planning")  # planning, active, completed, cancelled
