from pydantic import BaseModel


class BOMBase(BaseModel):
    product_name: str
    material_name: str
    quantity: int


class BOMCreate(BOMBase):
    pass


class BOMResponse(BOMBase):
    id: int
    
    class Config:
        orm_mode = True
