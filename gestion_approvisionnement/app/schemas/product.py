from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    stock_quantity: int = 0
    description: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    stock_quantity: int | None = None
    description: str | None = None
    is_active: bool | None = None

class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
