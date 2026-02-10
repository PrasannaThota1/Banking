from pydantic import BaseModel
from typing import Optional


class TransactionCreate(BaseModel):
    from_account: Optional[str]
    to_account: Optional[str]
    amount: float
    transaction_type: str


class TransactionOut(BaseModel):
    id: int
    from_account: Optional[str]
    to_account: Optional[str]
    amount: float
    transaction_type: str
    status: str

    class Config:
        from_attributes = True
