from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete
from typing import Optional
from app.model.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CRUDUser:
    @staticmethod
    async def get(db: AsyncSession, user_id: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user_in: UserCreate) -> User:
        hashed_password = pwd_context.hash(user_in.password)
        db_user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            middle_name=user_in.middle_name,
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=True,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def update(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
        data = user_in.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(user, key, value)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def soft_delete(db: AsyncSession, user: User) -> None:
        user.is_active = False
        db.add(user)
        await db.commit()
