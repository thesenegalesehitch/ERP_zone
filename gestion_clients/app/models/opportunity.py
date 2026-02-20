from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Opportunity(Base):
    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    value = Column(Float)
    stage = Column(String, default="prospecting")  # prospecting, proposal, negotiation, won, lost
    customer_id = Column(Integer)
