from typing import Optional
from pydantic import BaseModel, Field

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50, description="e.g. citizen, contractor, inspector, admin")
    description: Optional[str] = Field(None, max_length=255)

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True
