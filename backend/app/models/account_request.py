from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Text
from sqlalchemy.sql import func
from app.database.base import Base

class AccountRequest(Base):
    __tablename__ = "account_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_type = Column(String(50), nullable=False)
    branch = Column(String(150), nullable=True)
    initial_deposit = Column(Numeric(12,2), default=0)
    status = Column(String(50), default="PENDING_APPROVAL")
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
