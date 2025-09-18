from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut
from app.crud.role import CRUDRole
from app.api.v1.dependencies import get_current_user, require_roles
from app.database.session import get_db

router = APIRouter(prefix="/api", tags=["Роли"])

async def admin_required(current_user=Depends(get_current_user)):
    has_access = await require_roles(["admin"], current_user)
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return current_user

@router.get("/", response_model=List[RoleOut])
async def read_roles(db: AsyncSession = Depends(get_db), current_user=Depends(admin_required)):
    roles = await CRUDRole.get_all(db)
    return roles

@router.get("/{role_id}", response_model=RoleOut)
async def read_role(
    role_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(admin_required)
):
    role = await CRUDRole.get(db, str(role_id))
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")
    return role

@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(admin_required)
):
    role = await CRUDRole.create(db, role_in)
    return role

@router.put("/{role_id}", response_model=RoleOut)
async def update_role(
    role_id: uuid.UUID,
    role_in: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(admin_required)
):
    role = await CRUDRole.get(db, str(role_id))
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")
    updated_role = await CRUDRole.update(db, role, role_in)
    return updated_role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(admin_required)
):
    role = await CRUDRole.get(db, str(role_id))
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")
    await CRUDRole.delete(db, role)
