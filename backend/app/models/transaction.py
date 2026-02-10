from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    from_account = Column(String(50), nullable=True)
    to_account = Column(String(50), nullable=True)
    amount = Column(Numeric(12,2), nullable=False)
    transaction_type = Column(String(50), nullable=False)
    status = Column(String(50), default="COMPLETED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
