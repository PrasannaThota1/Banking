from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql import func
from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="USER")
    # Additional profile / KYC fields
    address = Column(String(500), nullable=True)
    dob = Column(String(50), nullable=True)
    government_id = Column(String(100), nullable=True)
    kyc_status = Column(String(50), default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
