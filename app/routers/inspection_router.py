from typing import List, Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.inspection_schema import (
    InspectionCreate,
    InspectionResponse,
    InspectionComplete
)
from app.services.inspection_service import InspectionService

router = APIRouter(prefix="/inspections", tags=["Inspection Scheduling & Alerts (Data Flow F3)"])

@router.get("/", response_model=List[InspectionResponse])
def list_inspections(db: Session = Depends(get_db)):
    """
    List all scheduled and completed road site inspections.
    """
    return InspectionService.get_all_inspections(db)

@router.post("/", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def schedule_inspection(inspection_in: InspectionCreate, db: Session = Depends(get_db)):
    """
    Schedule a new site inspection for a road segment or ongoing project.
    """
    return InspectionService.schedule_inspection(db, inspection_in)

@router.put("/{inspection_id}/complete", response_model=InspectionResponse)
def complete_inspection(
    inspection_id: int,
    complete_in: InspectionComplete,
    db: Session = Depends(get_db)
):
    """
    Record completed inspection findings, quality ratings, and reset road overdue status.
    """
    return InspectionService.complete_inspection(db, inspection_id, complete_in)

@router.post("/trigger-alert-scan", response_model=Dict[str, Any])
def trigger_inspection_alerts(db: Session = Depends(get_db)):
    """
    Data Flow F3: Background Inspection Alert Engine.
    Scans the database for roads not inspected within 30 days and dispatches alerts.
    """
    return InspectionService.check_and_trigger_overdue_alerts(db)
