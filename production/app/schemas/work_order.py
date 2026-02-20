from pydantic import BaseModel


class WorkOrderBase(BaseModel):
    product_name: str
    quantity: int
    status: str = "pending"


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrderResponse(WorkOrderBase):
    id: int
    
    class Config:
        orm_mode = True
