from fastapi import Depends, HTTPException, status
from typing import List
from app.model.user import User
from app.api.v1.dependencies import get_current_user  # или где объявлен get_current_user
from app.api.v1.dependencies import require_roles, require_permissions# если объявлены там

# Базовые зависимости
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Ролевые зависимости
def get_admin_user():
    return require_roles(["admin"])

def get_user():
    return require_roles(["user", "admin"])

# Пермишен-зависимости
def can_manage_users():
    return require_permissions(["users:write"])

def can_view_users():
    return require_permissions(["users:read"])

def can_manage_roles():
    return require_permissions(["roles:write"])
