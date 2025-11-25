import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schema.user_schema import UserCreate
from schema.token import Token
from crud.user_crud import get_user_by_email, create_user, verify_password

from app.database import get_db
from api.deps import LoginRequest
from auth.jwt import create_access_token
from crud.rbac_crud import get_permissions_for_role,get_user_direct_permissions

router = APIRouter(prefix="/api/auth", tags=["Auth"])



@router.post("/register", response_model=dict)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Email already registered"
        )

    create_user(
        db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name
    )

    return JSONResponse(
        content={
            "status_code": 200,
            "message": "User registered successfully."
        }
    )


@router.post("/token")
def token(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Step 1: Validate user credentials
    user = get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=" User Have Invalid credentials")

    # -------------------------------
    # Step 2: Load Hybrid RBAC Permissions
    # -------------------------------
    role_permissions = get_permissions_for_role(db, user.role.value)  # Role-based
    user_permissions = get_user_direct_permissions(db, user.id)        # User-specific

    # Combine permissions (union)
    combined_permissions = list(set(role_permissions).union(user_permissions))

    # -------------------------------
    # Step 3: Create JWT token with permissions
    # -------------------------------
    access_token = create_access_token(
        subject=user.email,
        user_id=user.id,
        role=user.role.value,
        permissions=combined_permissions
    )

    # Step 4: Return token and permissions
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_code": status.HTTP_200_OK,
            "message": "User login successfully",
            "data": {
                "access_token": access_token,
                "permissions": combined_permissions
            }
        }
    )