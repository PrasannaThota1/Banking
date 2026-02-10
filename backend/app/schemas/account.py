from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    account_type: str

class AccountOut(BaseModel):
    id: int
    user_id: int
    account_number: str
    account_type: str
    balance: float
    status: str

    class Config:
        from_attributes = True
