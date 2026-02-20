from pydantic import BaseModel
from typing import Optional


class StockBase(BaseModel):
    product_id: int
    quantity: int = 0
    reorder_level: int = 10


class StockCreate(StockBase):
    pass


class StockUpdate(BaseModel):
    quantity: Optional[int] = None
    reorder_level: Optional[int] = None


class StockResponse(StockBase):
    id: int
    
    class Config:
        orm_mode = True
