from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

from app.db.database import get_db
from app.db.models import User
password_hash = PasswordHash.recommended()

ALGORITHM = 'HS256'
security = HTTPBearer()


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security))-> int:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get('sub')

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token'
            )
        return int(user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token'
        )


async def get_current_user(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
) -> User:

    result = await db.execute(
        select(User).where(User.id == current_user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

async def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user



def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str)->bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: int)-> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        'sub': str(user_id),
        'exp': expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

