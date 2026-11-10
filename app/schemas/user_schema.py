from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    organization: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_name: str = "citizen"  # citizen, contractor, inspector, admin

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    roles: List[RoleResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
