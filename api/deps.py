from fastapi import Depends, HTTPException, status
from app.database import SessionLocal
from sqlalchemy.orm import Session
from auth.jwt import decode_token
from models.user import User, RoleEnum
from app.database import get_db
from fastapi.security import APIKeyHeader
from pydantic import EmailStr,BaseModel

api_key_scheme = APIKeyHeader(name="Authorization")


def get_current_user(token: str = Depends(api_key_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials.You Need To Login Again")
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def require_roles(*roles):
    def _checker(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return _checker


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
