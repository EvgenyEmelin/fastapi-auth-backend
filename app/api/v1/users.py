from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import UserOut, UserCreate, UserUpdate, UserBase
from app.crud.users import CRUDUser
from app.database.session import get_db

router = APIRouter(prefix="/api", tags=["Пользователи"])

@router.post("/", response_model=UserOut)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await CRUDUser.get_by_email(db, user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    user = await CRUDUser.create(db, user_in)
    return user

@router.get("/", response_model=List[UserBase])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    users = await CRUDUser.get_all(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserBase)
async def read_user(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        # Преобразуем строку в UUID, убирая кавычки если они есть
        user_uuid = UUID(user_id.strip('"'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await CRUDUser.get(db, user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await CRUDUser.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    updated_user = await CRUDUser.update(db, user, user_in)
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await CRUDUser.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    await CRUDUser.soft_delete(db, user)
