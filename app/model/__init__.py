# app/models/__init__.py
from app.model.base import Base
from app.model.role import Role
from app.model.permission import Permission
from app.model.role_permission import RolePermission
from app.model.user import User  # если у вас есть модель User

__all__ = ['Base', 'Role', 'Permission', 'RolePermission', 'User']