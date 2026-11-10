from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    action: str = Field(..., max_length=100, description="e.g. CREATE_REPORT, APPROVE_MILESTONE")
    entity_type: str = Field(..., max_length=50, description="e.g. RoadReport, RoadProject")
    entity_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    ip_address: Optional[str] = Field(None, max_length=45)

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogUpdate(BaseModel):
    action: Optional[str] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None

class AuditLogResponse(AuditLogBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
