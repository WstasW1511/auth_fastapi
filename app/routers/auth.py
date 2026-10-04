from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.schemas import UserRegistration, UserResponse, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, get_current_user_id

router = APIRouter(prefix='/v1', tags=['Auth'])

def normalize_phone(phone: str):

    if phone.startswith('8'):
        phone = phone[1:]
    if phone.startswith('+7'):
        phone = phone[2:]

    return phone


@router.post('/registration/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def registration(data: UserRegistration, db: AsyncSession = Depends(get_db)):

    phone = normalize_phone(data.phone)

    result = await db.execute(select(User).where(User.phone == phone))

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this phone alredy exist'
        )

    user = User(
        phone=phone,
        name=data.name,
        password=hash_password(data.password)
    )
    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


@router.post('/login/', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):

    phone = normalize_phone(data.phone)

    result = await db.execute(select(User).where(User.phone == phone))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect login or password",
        )

    check_password = verify_password(data.password, user.password)

    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect login or password'
        )
    user.inline = True

    await db.commit()
    await db.refresh(user)
    token = create_access_token(user.id)

    return {
        'access_token':token,
        'token_type': 'bearer'
    }


@router.post('/logout/', status_code=status.HTTP_200_OK)
async def logout(current_user_id: int=Depends(get_current_user_id), db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(User).where(User.id == current_user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    user.inline = False
    await db.commit()

    return {"message": "Successfully logged out"}