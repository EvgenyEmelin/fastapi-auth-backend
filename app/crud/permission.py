from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate

class CRUDPermission:
    @staticmethod
    async def get(db: AsyncSession, perm_id: str) -> Optional[Permission]:
        result = await db.execute(select(Permission).where(Permission.id == perm_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Permission]:
        result = await db.execute(select(Permission).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, perm_in: PermissionCreate) -> Permission:
        db_perm = Permission(
            resource=perm_in.resource,
            action=perm_in.action,
            description=perm_in.description,
        )
        db.add(db_perm)
        await db.commit()
        await db.refresh(db_perm)
        return db_perm

    @staticmethod
    async def update(db: AsyncSession, perm: Permission, perm_in: PermissionUpdate) -> Permission:
        data = perm_in.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(perm, key, value)
        db.add(perm)
        await db.commit()
        await db.refresh(perm)
        return perm

    @staticmethod
    async def delete(db: AsyncSession, perm: Permission) -> None:
        await db.delete(perm)
        await db.commit()
