from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.account import AccountCreate, AccountOut, AccountRequestCreate, AccountRequestOut, AdminCreateAccount
from app.models.user import User
from app.services.account_service import AccountService
from app.core.security import get_current_user, require_role

from types import SimpleNamespace

router = APIRouter()

@router.post('/create', response_model=AccountRequestOut)
async def create_account(payload: AccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Customers use this to create a REQUEST for a new account (pending admin approval)."""
    try:
        user_id = int(current_user.id)  # type: ignore
        # require KYC verified
        if getattr(current_user, 'kyc_status', None) != 'VERIFIED':
            raise Exception('KYC must be completed before requesting an account')
        req = AccountService.create_account_request(db, user_id, payload)
        return req
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


# Admin endpoints

@router.get('/requests', response_model=List[AccountRequestOut])
async def list_requests(db: Session = Depends(get_db), admin: User = Depends(require_role('ADMIN'))):
    return AccountService.get_pending_requests(db)


@router.post('/requests/{request_id}/approve', response_model=AccountOut)
async def approve_request(request_id: int, db: Session = Depends(get_db), admin: User = Depends(require_role('ADMIN'))):
    try:
        acc = AccountService.approve_request(db, request_id, int(getattr(admin, 'id')))
        return acc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/requests/{request_id}/reject', response_model=AccountRequestOut)
async def reject_request(request_id: int, payload: dict = Body(...), db: Session = Depends(get_db), admin: User = Depends(require_role('ADMIN'))):
    reason = payload.get('reason', 'Rejected by admin')
    try:
        req = AccountService.reject_request(db, request_id, reason, int(getattr(admin, 'id')))
        return req
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/admin/create', response_model=AccountOut)
async def admin_create(payload: AdminCreateAccount, db: Session = Depends(get_db), admin: User = Depends(require_role('ADMIN'))):
    try:
        acc = AccountService.admin_create_account(db, payload.user_id, payload.dict())
        return acc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

