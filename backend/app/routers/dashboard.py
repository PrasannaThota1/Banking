from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.services.account_service import AccountService
from app.core.security import get_current_user

router = APIRouter()

@router.get('/summary')
async def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = int(current_user.id)  # type: ignore
    summary = AccountService.get_dashboard_summary(db, user_id)
    return summary
