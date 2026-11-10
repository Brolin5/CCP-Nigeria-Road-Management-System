from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field

class InspectionBase(BaseModel):
    road_id: int
    project_id: Optional[int] = None
    inspector_id: Optional[int] = None
    scheduled_date: date
    conducted_date: Optional[date] = None
    status: str = Field(default="Scheduled", max_length=50)
    findings_summary: Optional[str] = None
    quality_rating: Optional[str] = Field(None, max_length=50)
    evidence_photos_json: Optional[str] = None
    alert_dispatched: bool = False

class InspectionCreate(InspectionBase):
    pass

class InspectionUpdate(BaseModel):
    conducted_date: Optional[date] = None
    status: Optional[str] = None
    findings_summary: Optional[str] = None
    quality_rating: Optional[str] = None
    evidence_photos_json: Optional[str] = None
    alert_dispatched: Optional[bool] = None
    alert_dispatched_at: Optional[datetime] = None

class InspectionResponse(InspectionBase):
    id: int
    alert_dispatched_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
