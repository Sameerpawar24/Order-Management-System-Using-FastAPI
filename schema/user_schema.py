from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field
from models.user import RoleEnum

password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]).{8,}$'

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: Annotated[str, Field(pattern=password_regex)]

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: RoleEnum
    is_active: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    full_name: Optional[str]
    is_active: Optional[bool]
    role: Optional[RoleEnum]
