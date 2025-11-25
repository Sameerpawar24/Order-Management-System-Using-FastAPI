from datetime import datetime, timedelta
from jose import jwt
from app.config import settings
from typing import Dict, List, Optional

# Create access token including Hybrid RBAC permissions
def create_access_token(
    subject: str,
    user_id: int,
    role: str,
    permissions: Optional[List[str]] = None,
    expires_delta: int = None
) -> str:

    if expires_delta is None:
        expires_delta = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    expire = datetime.utcnow() + timedelta(minutes=expires_delta)

    # Payload
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "user_id": user_id,
        "role": role,
        "permissions": permissions or []  
    }

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token


# Decode token
from jose import JWTError, jwt
def decode_token(token: str) -> Dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return {}
