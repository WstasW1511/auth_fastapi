from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserRole


async def init_roles(db: AsyncSession):
    roles = {
        1: "admin",
        2: "user",
    }

    for role_id, role_name in roles.items():

        result = await db.execute(
            select(UserRole).where(UserRole.id == role_id)
        )

        role = result.scalar_one_or_none()

        if role is None:
            db.add(
                UserRole(
                    id=role_id,
                    name=role_name
                )
            )

    await db.commit()