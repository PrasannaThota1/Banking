from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.account import AccountCreate, AccountOut
from app.models.user import User
from app.services.account_service import AccountService
from app.core.security import get_current_user

router = APIRouter()

@router.post('/create', response_model=AccountOut)
async def create_account(payload: AccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        user_id = int(current_user.id)  # type: ignore
        acc = AccountService.create_account(db, user_id, payload)
        return acc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/my-accounts', response_model=List[AccountOut])
async def my_accounts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = int(current_user.id)  # type: ignore
    accounts = AccountService.get_user_accounts(db, user_id)
    return accounts

@router.get('/{account_id}', response_model=AccountOut)
async def get_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    acc = AccountService.get_account(db, account_id)
    user_id = int(current_user.id)  # type: ignore
    if acc is None or int(acc.user_id) != user_id:  # type: ignore
        raise HTTPException(status_code=404, detail='Account not found')
    return acc

