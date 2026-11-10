from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ReportBase(BaseModel):
    report_type: str = Field(..., description="'defect' (e.g. pothole) or 'violation' (e.g. one-way driving)")
    category: str = Field(..., description="Pothole, Erosion, Flooded Road, One-Way Driving, Illegal Parking")
    description: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    location_description: Optional[str] = None
    photo_url: str = Field(..., description="Evidentiary photo URL")
    severity: str = "Medium" # Low, Medium, High, Critical
    road_id: Optional[int] = None

class ReportCreate(ReportBase):
    citizen_id: Optional[int] = None

class ReportStatusUpdate(BaseModel):
    status: str = Field(..., description="'Under Review', 'Assigned', 'Resolved', 'Rejected'")
    assigned_maintenance_team: Optional[str] = None

class ReportResponse(ReportBase):
    id: int
    ticket_number: str
    status: str
    is_duplicate: bool
    duplicate_of_id: Optional[int] = None
    citizen_id: Optional[int] = None
    assigned_maintenance_team: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ReportListResponse(BaseModel):
    total: int
    reports: List[ReportResponse]
