from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    project_code: str = Field(..., max_length=50, description="e.g. PRJ-2026-FCT-01")
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    road_id: int
    contractor_id: int
    supervising_agency: str = Field(default="Federal Ministry of Works", max_length=100)
    budget_naira: Optional[Decimal] = None
    start_date: Optional[date] = None
    expected_completion_date: Optional[date] = None
    current_progress_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    status: str = Field(default="Ongoing", max_length=50)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    contractor_id: Optional[int] = None
    supervising_agency: Optional[str] = None
    budget_naira: Optional[Decimal] = None
    start_date: Optional[date] = None
    expected_completion_date: Optional[date] = None
    current_progress_pct: Optional[float] = None
    status: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
