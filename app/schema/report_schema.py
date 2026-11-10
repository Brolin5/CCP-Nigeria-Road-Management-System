from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ReportBase(BaseModel):
    report_type: str = Field(default="defect", max_length=50)
    category: str = Field(..., max_length=100, description="e.g. Deep Pothole, Washout, Bridge Damage")
    description: Optional[str] = None
    latitude: float
    longitude: float
    location_description: Optional[str] = Field(None, max_length=255)
    photo_url: str = Field(..., max_length=500)
    severity: str = Field(default="Medium", max_length=50)
    status: str = Field(default="Pending", max_length=50)
    is_duplicate: bool = False
    duplicate_of_id: Optional[int] = None
    citizen_id: Optional[int] = None
    road_id: Optional[int] = None
    assigned_maintenance_team: Optional[str] = Field(None, max_length=100)

class ReportCreate(ReportBase):
    ticket_number: Optional[str] = Field(None, max_length=50, description="Auto-generated if omitted")

class ReportUpdate(BaseModel):
    category: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    is_duplicate: Optional[bool] = None
    duplicate_of_id: Optional[int] = None
    road_id: Optional[int] = None
    assigned_maintenance_team: Optional[str] = None
    resolved_at: Optional[datetime] = None

class ReportResponse(ReportBase):
    id: int
    ticket_number: str
    resolved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
