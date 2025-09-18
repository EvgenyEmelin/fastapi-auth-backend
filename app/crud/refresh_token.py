from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import uuid
from app.model.refresh_token import RefreshToken

class CRUDRefreshToken:
    @staticmethod
    async def create(db: AsyncSession, token: str, user_id: uuid.UUID) -> RefreshToken:
        db_token = RefreshToken(
            token=token,
            user_id=user_id,
            created_at=datetime.utcnow(),
            revoked=False
        )
        db.add(db_token)
        await db.commit()
        await db.refresh(db_token)
        return db_token

    @staticmethod
    async def get_by_token(db: AsyncSession, token: str) -> Optional[RefreshToken]:
        result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
        return result.scalar_one_or_none()

    @staticmethod
    async def revoke_token(db: AsyncSession, token: RefreshToken) -> None:
        token.revoked = True
        db.add(token)
        await db.commit()

    @staticmethod
    async def is_token_active(db: AsyncSession, token_str: str) -> bool:
        token = await CRUDRefreshToken.get_by_token(db, token_str)
        return token is not None and not token.revoked
