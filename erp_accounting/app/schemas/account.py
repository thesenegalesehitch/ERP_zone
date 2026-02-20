from pydantic import BaseModel
from typing import Optional


class AccountBase(BaseModel):
    name: str
    account_number: str
    account_type: str
    balance: float = 0.0


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[float] = None


class AccountResponse(AccountBase):
    id: int
    
    class Config:
        orm_mode = True
