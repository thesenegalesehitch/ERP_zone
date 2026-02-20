from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    stock: int = 0


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    
    class Config:
        orm_mode = True
