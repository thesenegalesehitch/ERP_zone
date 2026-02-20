from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    phone = Column(String)
    source = Column(String)
    status = Column(String, default="new")  # new, contacted, qualified, converted
