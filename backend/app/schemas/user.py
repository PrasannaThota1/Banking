from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str = ""
    password: str
    address: str | None = None
    dob: str | None = None
    government_id: str | None = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    role: str
    address: Optional[str]
    dob: Optional[str]
    government_id: Optional[str]
    kyc_status: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
