from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.schemas.role import RoleOut, RoleCreate, RoleUpdate
from app.schemas.permission import PermissionOut, PermissionCreate, PermissionUpdate
from app.crud.role import CRUDRole
from app.crud.permission import CRUDPermission
from app.crud.user_role import CRUDUserRole
from app.crud.role_permission import CRUDRolePermission
from app.database.session import get_db

router = APIRouter(prefix="/admin", tags=["Админка"])

@router.post("/roles/", response_model=RoleOut)
async def create_role(role_in: RoleCreate, db: AsyncSession = Depends(get_db)):
    roles = await CRUDRole.get_all(db)
    if any(r.name == role_in.name for r in roles):
        raise HTTPException(status_code=400, detail="Role exists")
    return await CRUDRole.create(db, role_in)

@router.get("/roles/", response_model=List[RoleOut])
async def read_roles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await CRUDRole.get_all(db, skip, limit)

@router.patch("/roles/{role_id}", response_model=RoleOut)
async def update_role(role_id: UUID, role_in: RoleUpdate, db: AsyncSession = Depends(get_db)):
    role = await CRUDRole.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return await CRUDRole.update(db, role, role_in)

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: UUID, db: AsyncSession = Depends(get_db)):
    role = await CRUDRole.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await CRUDRole.delete(db, role)

@router.post("/permissions/", response_model=PermissionOut)
async def create_permission(perm_in: PermissionCreate, db: AsyncSession = Depends(get_db)):
    perms = await CRUDPermission.get_all(db)
    if any(p.resource == perm_in.resource and p.action == perm_in.action for p in perms):
        raise HTTPException(status_code=400, detail="Permission exists")
    return await CRUDPermission.create(db, perm_in)

@router.get("/permissions/", response_model=List[PermissionOut])
async def read_permissions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await CRUDPermission.get_all(db, skip, limit)

@router.patch("/permissions/{perm_id}", response_model=PermissionOut)
async def update_permission(perm_id: UUID, perm_in: PermissionUpdate, db: AsyncSession = Depends(get_db)):
    perm = await CRUDPermission.get(db, perm_id)
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    return await CRUDPermission.update(db, perm, perm_in)

@router.delete("/permissions/{perm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(perm_id: UUID, db: AsyncSession = Depends(get_db)):
    perm = await CRUDPermission.get(db, perm_id)
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    await CRUDPermission.delete(db, perm)

@router.post("/user-roles/")
async def add_role_to_user(user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_db)):
    await CRUDUserRole.add_role_to_user(db, user_id, role_id)
    return {"detail": "Role added to user"}

@router.delete("/user-roles/")
async def remove_role_from_user(user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_db)):
    await CRUDUserRole.remove_role_from_user(db, user_id, role_id)
    return {"detail": "Role removed from user"}

@router.post("/role-permissions/")
async def add_permission_to_role(role_id: UUID, perm_id: UUID, db: AsyncSession = Depends(get_db)):
    await CRUDRolePermission.add_permission_to_role(db, role_id, perm_id)
    return {"detail": "Permission added to role"}

@router.delete("/role-permissions/")
async def remove_permission_from_role(role_id: UUID, perm_id: UUID, db: AsyncSession = Depends(get_db)):
    await CRUDRolePermission.remove_permission_from_role(db, role_id, perm_id)
    return {"detail": "Permission removed from role"}
