from pydantic import BaseModel
from typing import Optional


class WarehouseBase(BaseModel):
    name: str
    location: Optional[str] = None
    capacity: Optional[int] = None


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseResponse(WarehouseBase):
    id: int
    
    class Config:
        orm_mode = True
