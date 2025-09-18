from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.schemas.user import UserBase, UserCreate, UserUpdate
from app.crud.users import CRUDUser
from app.core.config import (
    get_current_active_user,
    get_admin_user,
    can_manage_users,
    can_view_users
)

router = APIRouter()


# Только аутентифицированные пользователи
@router.get("/me", response_model=UserBase)
async def read_user_me(current_user: UserBase = Depends(get_current_active_user)):
    return current_user


# Только админы могут видеть всех пользователей
@router.get("/", response_model=List[UserBase])
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        admin_user: UserBase = Depends(get_admin_user)  # Проверка роли
):
    users = await CRUDUser.get_all(db, skip=skip, limit=limit)
    return users


# Или с проверкой пермишенов
@router.get("/with-permissions", response_model=List[UserBase])
async def read_users_with_permissions(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        authorized_user: UserBase = Depends(can_view_users)  # Проверка прав
):
    users = await CRUDUser.get_all(db, skip=skip, limit=limit)
    return users


# Создание пользователя - только админы
@router.post("/", response_model=UserBase)
async def create_user(
        user_in: UserCreate,
        db: AsyncSession = Depends(get_db),
        admin_user: UserBase = Depends(get_admin_user)
):
    user = await CRUDUser.get_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists",
        )
    user = await CRUDUser.create(db, user_in)
    return user


# Просмотр конкретного пользователя - либо сам пользователь, либо админ
@router.get("/{user_id}", response_model=UserBase)
async def read_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_active_user)
):
    user = await CRUDUser.get(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Пользователь может смотреть только себя, админ - всех
    if str(current_user.id) != str(user_id) and "admin" not in [r.name for r in current_user.roles]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return user