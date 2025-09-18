from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from pydantic import BaseModel
from app.database.session import get_db
from app.crud.users import CRUDUser
from app.schemas.user import UserOut
from app.crud.refresh_token import CRUDRefreshToken

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class TokenData(BaseModel):
    email: Optional[str] = None

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен аутентификации",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    # Проверяем пользователя
    user = await CRUDUser.get_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception

    # Проверяем, что у пользователя есть неотозванный refresh токен
    result = await db.execute(
        select(CRUDRefreshToken.model).where(
            CRUDRefreshToken.model.user_id == user.id,
            CRUDRefreshToken.model.revoked == False  # поле revoked типа bool
        )
    )
    valid_token = result.scalars().first()
    if not valid_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    return user

async def require_roles(
    roles: List[str],
    current_user: UserOut = Depends(get_current_user)
):
    user_roles = {role.name for role in current_user.roles}
    if not user_roles.intersection(roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав: отсутствует необходимая роль"
        )
    return current_user

async def require_permissions(
    permissions: List[str],
    current_user: UserOut = Depends(get_current_user)
):
    user_permissions = set()
    for role in current_user.roles:
        user_permissions.update({perm.action for perm in role.permissions})
    if not user_permissions.intersection(permissions):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав: отсутствует необходимое право"
        )
    return current_user
