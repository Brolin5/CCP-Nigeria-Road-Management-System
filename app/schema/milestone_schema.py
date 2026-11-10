from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class MilestoneBase(BaseModel):
    project_id: int
    milestone_name: str = Field(..., max_length=150)
    milestone_order: int = Field(default=1, ge=1)
    percentage_weight: float = Field(default=0.0, ge=0.0, le=100.0)
    progress_pct_achieved: float = Field(default=0.0, ge=0.0, le=100.0)
    photo_evidence_url: Optional[str] = Field(None, max_length=500)
    contractor_notes: Optional[str] = None
    status: str = Field(default="Pending", max_length=50)

class MilestoneCreate(MilestoneBase):
    pass

class MilestoneUpdate(BaseModel):
    milestone_name: Optional[str] = None
    milestone_order: Optional[int] = None
    percentage_weight: Optional[float] = None
    progress_pct_achieved: Optional[float] = None
    photo_evidence_url: Optional[str] = None
    contractor_notes: Optional[str] = None
    status: Optional[str] = None
    submitted_at: Optional[datetime] = None
    inspected_at: Optional[datetime] = None

class MilestoneResponse(MilestoneBase):
    id: int
    submitted_at: Optional[datetime] = None
    inspected_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
