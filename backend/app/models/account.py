from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_number = Column(String(50), unique=True, index=True, nullable=False)
    account_type = Column(String(50), default="SAVINGS")
    balance = Column(Numeric(12,2), default=0)
    branch = Column(String(150), nullable=True)
    ifsc = Column(String(50), nullable=True)
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User")
