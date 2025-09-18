from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.role import Role
from app.schemas.role import RoleCreate, RoleUpdate

class CRUDRole:
    @staticmethod
    async def get(db: AsyncSession, role_id: str) -> Optional[Role]:
        result = await db.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Role]:
        result = await db.execute(select(Role).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, role_in: RoleCreate) -> Role:
        db_role = Role(
            name=role_in.name,
            description=role_in.description,
        )
        db.add(db_role)
        await db.commit()
        await db.refresh(db_role)
        return db_role

    @staticmethod
    async def update(db: AsyncSession, role: Role, role_in: RoleUpdate) -> Role:
        data = role_in.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(role, key, value)
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def delete(db: AsyncSession, role: Role) -> None:
        await db.delete(role)
        await db.commit()
