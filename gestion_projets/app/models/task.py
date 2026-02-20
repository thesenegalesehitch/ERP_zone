from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    project_id = Column(Integer)
    status = Column(String, default="todo")  # todo, in_progress, done
