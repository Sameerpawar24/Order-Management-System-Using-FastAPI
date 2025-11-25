import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from functools import wraps

from app.database import get_db
from auth.jwt import decode_token
from models.user import User
from crud.rbac_crud import get_effective_permissions
from pydantic import BaseModel, EmailStr

api_key_scheme = APIKeyHeader(name="Authorization")


def get_current_user(
    token: str = Depends(api_key_scheme), 
    db: Session = Depends(get_db)) -> User:

    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your Token is Invalid or expired",
        )
    user_id = payload.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user



def require_permission(permission_name: str):
    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        # Load Hybrid RBAC permissions
        effective = get_effective_permissions(db, current_user.id, current_user.role.value)

        if permission_name not in effective:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: missing permission"
            )
        return current_user
    return dependency



# Login Payload
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
