from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/banking_db"
    COOKIE_DOMAIN: str | None = None
    COOKIE_PATH: str = "/"
    COOKIE_SAMESITE: Literal['lax', 'strict', 'none'] = "none"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
