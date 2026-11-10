from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class InspectionBase(BaseModel):
    road_id: int
    project_id: Optional[int] = None
    inspector_id: Optional[int] = None
    scheduled_date: date

class InspectionCreate(InspectionBase):
    pass

class InspectionComplete(BaseModel):
    conducted_date: date
    findings_summary: str
    quality_rating: str = Field(..., description="'Satisfactory', 'Minor Defects', 'Critical Non-Compliance'")
    evidence_photos_json: Optional[str] = None

class InspectionResponse(InspectionBase):
    id: int
    conducted_date: Optional[date] = None
    status: str
    findings_summary: Optional[str] = None
    quality_rating: Optional[str] = None
    alert_dispatched: bool
    alert_dispatched_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class OverdueRoadResponse(BaseModel):
    id: int
    road_code: str
    name: str
    classification: str
    state: str
    lga: Optional[str] = None
    condition_status: str
    last_inspected_at: Optional[datetime] = None
    days_since_last_inspection: Optional[int] = None

    class Config:
        from_attributes = True
