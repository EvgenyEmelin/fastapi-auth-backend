from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.user_role import UserRole
import uuid

class CRUDUserRole:
    @staticmethod
    async def add_role_to_user(db: AsyncSession, user_id: uuid.UUID, role_id: uuid.UUID):
        user_role = UserRole(user_id=user_id, role_id=role_id)
        db.add(user_role)
        await db.commit()

    @staticmethod
    async def remove_role_from_user(db: AsyncSession, user_id: uuid.UUID, role_id: uuid.UUID):
        result = await db.execute(
            select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
        )
        user_role = result.scalar_one_or_none()
        if user_role:
            await db.delete(user_role)
            await db.commit()
