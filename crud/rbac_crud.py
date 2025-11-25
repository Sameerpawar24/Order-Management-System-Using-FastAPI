from sqlalchemy.orm import Session
from models.permission import Permission
from models.role_permission import RolePermission
from models.user_permission import UserPermission
from typing import Set

# Role permissions
def get_permissions_for_role(db: Session, role_name: str) -> Set[str]:
    rows = (
        db.query(Permission.name)
        .join(RolePermission, Permission.id == RolePermission.permission_id)
        .filter(RolePermission.role_name == role_name)
        .all()
    )
    return {r[0] for r in rows}

# User direct permissions
def get_user_direct_permissions(db: Session, user_id: int) -> Set[str]:
    rows = (
        db.query(Permission.name, UserPermission.is_allowed)
        .join(UserPermission, Permission.id == UserPermission.permission_id)
        .filter(UserPermission.user_id == user_id)
        .all()
    )
    return {r[0] for r in rows if r[1]}

# Effective permissions = role + user direct
def get_effective_permissions(db: Session, user_id: int, role_name: str) -> Set[str]:
    role_perms = get_permissions_for_role(db, role_name)
    user_perms = get_user_direct_permissions(db, user_id)
    return role_perms.union(user_perms)

# Assign permission to role
def assign_permission_to_role(db: Session, role_name: str, perm: Permission):
    from models.role_permission import RolePermission
    exists = db.query(RolePermission).filter(RolePermission.role_name==role_name, RolePermission.permission_id==perm.id).first()
    if exists:
        return exists
    rp = RolePermission(role_name=role_name, permission_id=perm.id)
    db.add(rp)
    db.commit()
    db.refresh(rp)
    return rp

# Assign permission to user
def assign_permission_to_user(db: Session, user_id: int, perm: Permission, is_allowed: bool=True):
    exists = db.query(UserPermission).filter(UserPermission.user_id==user_id, UserPermission.permission_id==perm.id).first()
    if exists:
        exists.is_allowed = is_allowed
        db.add(exists)
        db.commit()
        db.refresh(exists)
        return exists
    up = UserPermission(user_id=user_id, permission_id=perm.id, is_allowed=is_allowed)
    db.add(up)
    db.commit()
    db.refresh(up)
    return up

# Create permission if not exist
def create_permission(db: Session, name: str, description: str=None):
    perm = db.query(Permission).filter(Permission.name==name).first()
    if perm:
        return perm
    perm = Permission(name=name, description=description)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm




