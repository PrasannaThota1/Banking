from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserOut, UserUpdate
from app.models.user import User
from app.services.auth_service import AuthService
from app.core.security import get_current_user

router = APIRouter()

@router.get('/profile', response_model=UserOut)
async def profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put('/profile', response_model=UserOut)
async def update_profile(payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = int(current_user.id)  # type: ignore
    user = AuthService.update_profile(db, user_id, payload.name, payload.phone)
    return user

