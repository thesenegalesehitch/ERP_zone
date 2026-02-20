from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    status: str = "todo"


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    
    class Config:
        orm_mode = True
