from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.report_schema import (
    ReportCreate,
    ReportResponse,
    ReportStatusUpdate,
    ReportListResponse
)
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Citizen Reporting & Triage (Data Flow F1 & F4)"])

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def submit_report(report_in: ReportCreate, db: Session = Depends(get_db)):
    """
    Data Flow F1: Citizen Crowdsourced Defect / Traffic Violation Submission.
    Automatically checks for existing reports within a 100-meter radius to detect duplicates.
    """
    return ReportService.create_report(db, report_in)

@router.get("/", response_model=ReportListResponse)
def list_reports(
    report_type: Optional[str] = Query(None, description="'defect' or 'violation'"),
    category: Optional[str] = Query(None, description="Pothole, Erosion, etc."),
    status_filter: Optional[str] = Query(None, description="Pending, Under Review, Assigned, Resolved, Duplicate"),
    road_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Retrieve reports with optional filtering by type, category, status, and road asset.
    """
    items = ReportService.get_reports(
        db, report_type=report_type, category=category,
        status_filter=status_filter, road_id=road_id,
        skip=skip, limit=limit
    )
    return {"total": len(items), "reports": items}

@router.get("/{ticket_number}", response_model=ReportResponse)
def track_report_by_ticket(ticket_number: str, db: Session = Depends(get_db)):
    """
    Allows citizens and officials to track report status using their unique tracking ticket number.
    """
    return ReportService.get_report_by_ticket(db, ticket_number)

@router.patch("/{report_id}/status", response_model=ReportResponse)
def update_status(report_id: int, update_in: ReportStatusUpdate, db: Session = Depends(get_db)):
    """
    Data Flow F4: Administrative Triage.
    Allows officials to transition ticket status (e.g., 'Under Review' -> 'Assigned' -> 'Resolved')
    and dispatch maintenance teams.
    """
    return ReportService.update_report_status(db, report_id, update_in)
