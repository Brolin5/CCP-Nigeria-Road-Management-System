from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class RoadBase(BaseModel):
    road_code: str = Field(..., max_length=50, description="e.g. FED-A234-ABJ")
    name: str = Field(..., max_length=150, description="e.g. Abuja-Keffi Dual Carriageway")
    classification: str = Field(default="Federal", max_length=50)
    state: str = Field(..., max_length=50)
    lga: Optional[str] = Field(None, max_length=100)
    length_km: Optional[float] = None
    start_latitude: Optional[float] = None
    start_longitude: Optional[float] = None
    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    condition_status: str = Field(default="Fair", max_length=50)
    is_inspection_overdue: bool = False

class RoadCreate(RoadBase):
    pass

class RoadUpdate(BaseModel):
    name: Optional[str] = None
    classification: Optional[str] = None
    state: Optional[str] = None
    lga: Optional[str] = None
    length_km: Optional[float] = None
    start_latitude: Optional[float] = None
    start_longitude: Optional[float] = None
    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    condition_status: Optional[str] = None
    last_inspected_at: Optional[datetime] = None
    is_inspection_overdue: Optional[bool] = None

class RoadResponse(RoadBase):
    id: int
    last_inspected_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
