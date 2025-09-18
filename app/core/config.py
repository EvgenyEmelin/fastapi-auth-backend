from fastapi import Depends, HTTPException
from app.middleware.auth_middleware import (
    get_current_user,
    required_roles,
    required_permissions
)
from app.model.user import User

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    # другие параметры

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()



# Базовые зависимости
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Ролевые зависимости
def get_admin_user():
    return required_roles(["admin"])

def get_user():
    return required_roles(["user", "admin"])

# Пермишен-зависимости
def can_manage_users():
    return required_permissions(["users:write"])

def can_view_users():
    return required_permissions(["users:read"])

def can_manage_roles():
    return required_permissions(["roles:write"])
