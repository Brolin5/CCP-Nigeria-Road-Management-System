from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# Milestone Schemas
class MilestoneBase(BaseModel):
    milestone_name: str
    milestone_order: int = 1
    percentage_weight: float = Field(..., ge=0, le=100)

class MilestoneCreate(MilestoneBase):
    pass

class MilestoneProgressUpdate(BaseModel):
    progress_pct_achieved: float = Field(..., ge=0, le=100)
    photo_evidence_url: str = Field(..., description="Mandatory timestamped progress photo URL")
    contractor_notes: Optional[str] = None

class MilestoneReview(BaseModel):
    status: str = Field(..., description="'Approved', 'Rejected', 'Pending Inspection'")

class MilestoneResponse(MilestoneBase):
    id: int
    project_id: int
    progress_pct_achieved: float
    photo_evidence_url: Optional[str] = None
    contractor_notes: Optional[str] = None
    status: str
    submitted_at: Optional[datetime] = None
    inspected_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    project_code: str
    title: str
    description: Optional[str] = None
    road_id: int
    contractor_id: int
    supervising_agency: str = "Federal Ministry of Works / FERMA"
    budget_naira: Optional[float] = None
    start_date: Optional[date] = None
    expected_completion_date: Optional[date] = None

class ProjectCreate(ProjectBase):
    milestones: Optional[List[MilestoneCreate]] = None

class ProjectResponse(ProjectBase):
    id: int
    current_progress_pct: float
    status: str
    created_at: datetime
    milestones: List[MilestoneResponse] = []

    class Config:
        from_attributes = True
