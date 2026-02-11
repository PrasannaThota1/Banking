from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserOut, UserUpdate
from app.models.user import User
from app.services.auth_service import AuthService
from app.core.security import get_current_user, require_role

router = APIRouter()

@router.get('/profile', response_model=UserOut)
async def profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put('/profile', response_model=UserOut)
async def update_profile(payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = int(current_user.id)  # type: ignore
    user = AuthService.update_profile(db, user_id, payload.name, payload.phone)
    return user


@router.post('/admin/users/{user_id}/kyc')
async def admin_set_kyc(user_id: int, payload: dict = Body(...), db: Session = Depends(get_db), admin: User = Depends(require_role('ADMIN'))):
    status = payload.get('status')
    if status not in ('PENDING', 'VERIFIED', 'REJECTED'):
        raise HTTPException(status_code=400, detail='Invalid KYC status')
    try:
        user = AuthService.set_kyc_status(db, user_id, status)
        return {"msg": "KYC status updated", "user": {"id": user.id, "kyc_status": getattr(user, 'kyc_status', None)}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/admin/list')
async def admin_list_users(db: Session = Depends(get_db), admin: User = Depends(require_role('ADMIN'))):
    try:
        users = AuthService.get_all_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

