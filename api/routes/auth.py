from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import UserCreate
from fastapi.responses import JSONResponse
from crud.user_crud import get_user_by_email, create_user, verify_password
from app.database import SessionLocal
from schema.token import Token
from auth.jwt import create_access_token
from app.database import get_db
from sqlalchemy.orm import Session
from api.deps import LoginRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=dict)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")
    user = create_user(db, email=payload.email, password=payload.password, full_name=payload.full_name)
    return JSONResponse(content={"status_code":200,"messege": "User Register successfully."})


@router.post("/token", response_model=Token)
def token(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Step 1: find user
    user = get_user_by_email(db, login_data.email)

    # Step 2: validate credentials
    if not user or not verify_password(login_data.password, user.hashed_password):
        return JSONResponse(
            content={"status_code":status.HTTP_401_UNAUTHORIZED,'messege':"Invalid Credentials"}
        )
    # Step 3: create token
    access_token = create_access_token(
        subject=user.email,
        user_id=user.id,
        role=user.role.value
    )
    # Step 4: return token
    return JSONResponse(content={"status_code":status.HTTP_200_OK,'messege':"User Login Successfully",'data':{'access_token':access_token}})
