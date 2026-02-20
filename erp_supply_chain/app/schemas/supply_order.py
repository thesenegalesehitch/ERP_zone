from pydantic import BaseModel


class SupplyOrderBase(BaseModel):
    product_name: str
    quantity: int
    supplier: str = ""
    status: str = "pending"


class SupplyOrderCreate(SupplyOrderBase):
    pass


class SupplyOrderResponse(SupplyOrderBase):
    id: int
    
    class Config:
        orm_mode = True
