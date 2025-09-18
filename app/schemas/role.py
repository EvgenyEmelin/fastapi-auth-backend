from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class RoleOut(RoleBase):
    id: UUID

    class Config:
        orm_mode = True
