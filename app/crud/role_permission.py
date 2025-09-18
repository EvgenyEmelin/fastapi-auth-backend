from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.role_permission import RolePermission
import uuid

class CRUDRolePermission:
    @staticmethod
    async def add_permission_to_role(db: AsyncSession, role_id: uuid.UUID, perm_id: uuid.UUID):
        role_perm = RolePermission(role_id=role_id, permission_id=perm_id)
        db.add(role_perm)
        await db.commit()

    @staticmethod
    async def remove_permission_from_role(db: AsyncSession, role_id: uuid.UUID, perm_id: uuid.UUID):
        result = await db.execute(
            select(RolePermission).where(RolePermission.role_id == role_id, RolePermission.permission_id == perm_id)
        )
        role_perm = result.scalar_one_or_none()
        if role_perm:
            await db.delete(role_perm)
            await db.commit()

    @staticmethod
    async def get_permissions_by_role(db: AsyncSession, role_id: uuid.UUID) -> List[uuid.UUID]:
        result = await db.execute(
            select(RolePermission.permission_id).where(RolePermission.role_id == role_id)
        )
        return [row[0] for row in result.all()]
