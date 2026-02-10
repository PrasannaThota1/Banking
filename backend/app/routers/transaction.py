from typing import List
from fastapi import APIRouter, Depends, HTTPException
from decimal import Decimal
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.services.account_service import AccountService
from app.core.security import get_current_user
from app.schemas.transaction import TransactionOut

router = APIRouter()

class DepositRequest(BaseModel):
    to_account: str
    amount: float

class WithdrawRequest(BaseModel):
    from_account: str
    amount: float

class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float
    idempotency_key: str | None = None

@router.post('/deposit')
async def deposit(payload: DepositRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        user_id = int(current_user.id)  # type: ignore
        result = AccountService.deposit(db, user_id, payload.to_account, Decimal(str(payload.amount)))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/withdraw')
async def withdraw(payload: WithdrawRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        user_id = int(current_user.id)  # type: ignore
        result = AccountService.withdraw(db, user_id, payload.from_account, Decimal(str(payload.amount)))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/transfer')
async def transfer(payload: TransferRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        user_id = int(current_user.id)  # type: ignore
        result = AccountService.transfer(
            db, 
            user_id, 
            payload.from_account, 
            payload.to_account, 
            Decimal(str(payload.amount)),
            payload.idempotency_key
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/history', response_model=List[TransactionOut])
async def history(limit: int = 50, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = int(current_user.id)  # type: ignore
    txns = AccountService.get_history(db, user_id, limit)
    return txns

