from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    account_type: str
    branch: Optional[str] = None
    initial_deposit: Optional[float] = 0.0

class AccountOut(BaseModel):
    id: int
    user_id: int
    account_number: str
    account_type: str
    balance: float
    status: str

    class Config:
        from_attributes = True


class AccountRequestCreate(BaseModel):
    account_type: str
    branch: Optional[str] = None
    initial_deposit: Optional[float] = 0.0


class AccountRequestOut(BaseModel):
    id: int
    user_id: int
    account_type: str
    branch: Optional[str]
    initial_deposit: float
    status: str
    reason: Optional[str]

    class Config:
        from_attributes = True


class AdminCreateAccount(BaseModel):
    user_id: int
    account_type: str
    branch: Optional[str] = None
    initial_deposit: Optional[float] = 0.0
