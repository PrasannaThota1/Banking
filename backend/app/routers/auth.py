from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, Header, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import AuthService
from app.core.config import settings

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post('/register', response_model=UserOut)
async def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = AuthService.register(db, payload)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/login')
async def login(response: Response, payload: LoginRequest, db: Session = Depends(get_db)):
    result = AuthService.login(db, payload.email, payload.password)
    if not result:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    response.set_cookie(
        key='access_token',
        value=result['access_token'],
        httponly=True,
        secure=False,  # Set to True in production (HTTPS)
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path=settings.COOKIE_PATH,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key='refresh_token',
        value=result['refresh_token'],
        httponly=True,
        secure=False,  # Set to True in production (HTTPS)
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path=settings.COOKIE_PATH,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
    )
    # Also return tokens in response body so frontend can store them in localStorage
    return {
        "msg": "Logged in successfully",
        "user": result['user'],
        "access_token": result['access_token'],
        "refresh_token": result['refresh_token']
    }

@router.post('/refresh-token')
async def refresh(response: Response, payload: RefreshRequest):
    result = AuthService.refresh(payload.refresh_token)
    if not result:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    
    response.set_cookie(
        key='access_token',
        value=result['access_token'],
        httponly=True,
        secure=False,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path=settings.COOKIE_PATH,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    # Return new access token for frontend usage as well
    return {"msg": "Token refreshed", "access_token": result['access_token']}

@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token', path=settings.COOKIE_PATH, domain=settings.COOKIE_DOMAIN)
    response.delete_cookie('refresh_token', path=settings.COOKIE_PATH, domain=settings.COOKIE_DOMAIN)
    return {"msg": "Logged out successfully"}


@router.get('/debug-token')
async def debug_token(access_token: str | None = Cookie(None), authorization: str | None = Header(None)):
    """Temporary debug endpoint: returns decoded JWT payload from cookie or Authorization header."""
    token = access_token
    if not token and authorization and authorization.startswith('Bearer '):
        token = authorization.split(' ', 1)[1]
    from app.core.security import decode_token
    print("DEBUG /auth/debug-token: incoming cookie access_token:", access_token, "Authorization header:", authorization)
    if not token:
        raise HTTPException(status_code=401, detail='No token provided')
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    return {"payload": payload}


@router.get('/debug-headers')
async def debug_headers(request: Request):
    """Public debug endpoint: shows all headers received by the backend."""
    headers_dict = {key: value for key, value in request.headers.items()}
    print("\n=== DEBUG /auth/debug-headers ===")
    for key, value in headers_dict.items():
        print(f"  {key}: {value}")
    print("==================================\n")
    return {
        "all_headers": headers_dict,
        "authorization": headers_dict.get('authorization'),
        "cookie": headers_dict.get('cookie')
    }

