from pydantic import BaseModel


class SaleBase(BaseModel):
    product_name: str
    quantity: int
    total: float
    payment_method: str = ""


class SaleCreate(SaleBase):
    pass


class SaleResponse(SaleBase):
    id: int
    
    class Config:
        orm_mode = True
