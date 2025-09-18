from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class PermissionBase(BaseModel):
    resource: str = Field(..., min_length=1, max_length=50)
    action: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    resource: Optional[str]
    action: Optional[str]
    description: Optional[str]

class PermissionOut(PermissionBase):
    id: UUID

    class Config:
        orm_mode = True
