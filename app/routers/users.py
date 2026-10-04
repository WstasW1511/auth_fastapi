from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.core.security import get_current_user_id, get_current_admin
from app.schemas import GetUsers

router = APIRouter(
    prefix='/v1/users',
    tags=['Users']
)


@router.get('/', response_model=list[GetUsers])
async def get_users(current_admin: User = Depends(get_current_admin), db: AsyncSession=Depends(get_db)):
    result = await db.execute(select(User))

    users = result.scalars().all()

    return users

