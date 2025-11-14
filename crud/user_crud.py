import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from sqlalchemy.orm import Session
# from models.user import User, RoleEnum
from passlib.context import CryptContext
from models.user import User, RoleEnum
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str, full_name: str = None, role: RoleEnum = RoleEnum.customer):
    hashed = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed, full_name=full_name, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
