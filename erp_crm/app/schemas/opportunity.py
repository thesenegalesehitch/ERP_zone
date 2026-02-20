from pydantic import BaseModel
from typing import Optional


class OpportunityBase(BaseModel):
    name: str
    value: Optional[float] = None
    stage: str = "prospecting"
    customer_id: Optional[int] = None


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityResponse(OpportunityBase):
    id: int
    
    class Config:
        orm_mode = True
