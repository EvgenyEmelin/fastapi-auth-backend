from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database.session import get_db
from app.crud.users import CRUDUser
from app.model.user import User
from app.crud.refresh_token import CRUDRefreshToken

# Импорт settings отложENO для исключения циклического импорта
def get_settings():
    from app.core.config import settings
    return settings

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db),
        settings = Depends(get_settings)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await CRUDUser.get_by_email(db, email)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Проверяем, что пользователь имеет неотозванный refresh токен
    result = await db.execute(
        select(CRUDRefreshToken.model).where(
            CRUDRefreshToken.model.user_id == user.id,
            CRUDRefreshToken.model.revoked == False
        )
    )
    valid_token = result.scalars().first()
    if valid_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    return user


def required_roles(required_roles: List[str]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        user_roles = [role.name for role in current_user.roles]

        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user

    return role_checker


def required_permissions(required_permissions: List[str]):
    async def permission_checker(
            current_user: User = Depends(get_current_user),
            db: AsyncSession = Depends(get_db)
    ):
        user_permissions = []
        for role in current_user.roles:
            for role_perm in role.role_permissions:
                permission = f"{role_perm.permission.resource}:{role_perm.permission.action}"
                user_permissions.append(permission)

        if not any(perm in user_permissions for perm in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user

    return permission_checker


def admin_required():
    return required_roles(["admin"])


def user_required():
    return required_roles(["user", "admin"])
