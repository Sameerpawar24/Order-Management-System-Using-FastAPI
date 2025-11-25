from pydantic import BaseModel
from typing import Optional

class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class AssignRolePermissionSchema(BaseModel):
    role_name: str
    permission_name: str

class AssignUserPermissionSchema(BaseModel):
    user_id: int
    permission_name: str
    is_allowed: Optional[bool] = True

class PermissionRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
