from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from app.schemas.user import UserCreate

class AuthService:
    @staticmethod
    def register(db: Session, payload: UserCreate):
        user = db.query(User).filter(User.email == payload.email).first()
        if user:
            raise Exception('User already exists')
        new = User(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            address=getattr(payload, 'address', None),
            dob=getattr(payload, 'dob', None),
            government_id=getattr(payload, 'government_id', None),
            password_hash=get_password_hash(payload.password),
            role="USER",
            kyc_status="PENDING"
        )
        db.add(new)
        db.commit()
        db.refresh(new)
        return new

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        data = {"sub": str(user.id), "role": user.role}
        return {
            "access_token": create_access_token(data), 
            "refresh_token": create_refresh_token(data),
            "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
        }

    @staticmethod
    def refresh(refresh_token: str):
        payload = decode_token(refresh_token)
        if not payload:
            return None
        data = {"sub": payload.get('sub'), "role": payload.get('role')}
        return {"access_token": create_access_token(data)}

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.get(User, user_id)

    @staticmethod
    def update_profile(db: Session, user_id: int, name: Optional[str] = None, phone: Optional[str] = None):
        user = db.get(User, user_id)
        if not user:
            raise Exception('User not found')
        if name:
            user.name = name  # type: ignore
        if phone:
            user.phone = phone  # type: ignore
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def set_kyc_status(db: Session, user_id: int, status: str):
        user = db.get(User, user_id)
        if not user:
            raise Exception('User not found')
        user.kyc_status = status  # type: ignore
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()
