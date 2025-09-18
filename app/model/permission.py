import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
from app.model.base import Base

if TYPE_CHECKING:
    from app.model.role_permission import RolePermission
    from app.model.role import Role


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    resource: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Отношение через ассоциативную модель
    role_permissions: Mapped[list["RolePermission"]] = relationship("RolePermission", back_populates="permission")
