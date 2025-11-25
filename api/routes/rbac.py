from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User, RoleEnum
from app.database import get_db
from deps import require_permission
from crud.rbac_crud import create_permission, assign_permission_to_role, assign_permission_to_user, get_effective_permissions, get_permissions_for_role

router = APIRouter(prefix="/api/rbac", tags=["Role Based Access"])

@router.post("/assign-role/{user_id}")
def assign_role(user_id: int, role: RoleEnum, db: Session = Depends(get_db),
                current_user: User = Depends(require_permission("user.assign_role"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    db.add(user)
    db.commit()
    return {"status_code": 200, "details":{"message": f"Role '{role}' assigned to user {user.email}"}}

@router.post("/role-permission")
def assign_perm_to_role(role_name: RoleEnum, permission_name: str, db: Session = Depends(get_db),
                        current_user: User = Depends(require_permission("role.assign_permission"))):
    perm = create_permission(db, permission_name)
    assign_permission_to_role(db, role_name.value, perm)
    return {"status_code": 200, "details":{"message": f"Permission '{permission_name}' assigned to role '{role_name}'"}}

@router.post("/user-permission")
def assign_perm_to_user_endpoint(user_id: int, permission_name: str, is_allowed: bool = True,
                                 db: Session = Depends(get_db),
                                 current_user: User = Depends(require_permission("user.assign_permission"))):
    perm = create_permission(db, permission_name)
    assign_permission_to_user(db, user_id, perm, is_allowed)
    status = "granted" if is_allowed else "revoked"
    return {"status_code": 200, "details":{"message": f"Permission '{permission_name} {status} for user {user_id}"}}

@router.get("/user/{user_id}/permissions")
def list_user_permissions(user_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(require_permission("user.view_permissions"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    effective = get_effective_permissions(db, user_id, user.role.value)
    return {'status_code':200,'details':{"user_id": user_id, "permissions": list(effective)}}

@router.get("/role/{role_name}/permissions")
def list_role_permissions(role_name: RoleEnum, db: Session = Depends(get_db),
                          current_user: User = Depends(require_permission("role.view_permissions"))):
    perms = get_permissions_for_role(db, role_name.value)
    return {'status_code':200,'details':{"role": role_name, "permissions": list(perms)}}




# # app/api/routes/rbac.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from api.deps import get_current_user, get_db, require_permission
# from schema.rbac import PermissionCreate, AssignRolePermissionSchema, AssignUserPermissionSchema, PermissionRead
# from crud import rbac_crud
# from models.user import RoleEnum

# router = APIRouter(prefix="/api/rbac", tags=["rbac"])

# # admin-only: create permission
# @router.post("/permissions", response_model=PermissionRead, dependencies=[Depends(require_roles(RoleEnum.admin.value))])
# def create_permission(payload: PermissionCreate, db: Session = Depends(get_db)):
#     perm = rbac_crud.create_permission(db, payload.name, payload.description)
#     return perm

# # admin-only: assign permission to role
# @router.post("/roles/permissions", dependencies=[Depends(require_roles(RoleEnum.admin.value))])
# def assign_perm_to_role(payload: AssignRolePermissionSchema, db: Session = Depends(get_db)):
#     perm = rbac_crud.get_permission_by_name(db, payload.permission_name)
#     if not perm:
#         raise HTTPException(status_code=404, detail="Permission not found")
#     rp = rbac_crud.assign_permission_to_role(db, payload.role_name, perm)
#     return {"role": payload.role_name, "permission": perm.name}

# # admin-only: assign permission to user (user-specific override)
# @router.post("/users/permissions", dependencies=[Depends(require_roles(RoleEnum.admin.value))])
# def assign_perm_to_user(payload: AssignUserPermissionSchema, db: Session = Depends(get_db)):
#     perm = rbac_crud.get_permission_by_name(db, payload.permission_name)
#     if not perm:
#         raise HTTPException(status_code=404, detail="Permission not found")
#     up = rbac_crud.assign_permission_to_user(db, payload.user_id, perm, payload.is_allowed)
#     return {"user_id": payload.user_id, "permission": perm.name, "is_allowed": bool(payload.is_allowed)}
