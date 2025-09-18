import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
from app.model.base import Base

if TYPE_CHECKING:
    from app.model.user import User
    from app.model.role_permission import RolePermission
    from app.model.permission import Permission


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Отношение через ассоциативную модель
    role_permissions: Mapped[list["RolePermission"]] = relationship("RolePermission", back_populates="role")


    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )