from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.report_controller import report_controller
from app.schema.report_schema import ReportCreate, ReportUpdate, ReportResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED, summary="Insert Report")
def insert_report(payload: ReportCreate, db: Session = Depends(get_db)):
    """Insert a new crowdsourced road defect/violation report."""
    return report_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[ReportResponse], summary="Paginate Reports")
def get_reports_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch defect reports with pagination."""
    return report_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[ReportResponse], summary="Search Reports Real-Time")
def search_reports(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search reports in real-time across ticket number, category, description, location, or severity."""
    return report_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/{id}", response_model=ReportResponse, summary="Get Report by ID")
def get_report_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single report by primary key ID."""
    return report_controller.get_by_id(id, db)

@router.put("/{id}", response_model=ReportResponse, summary="Update Report")
def update_report(id: int, payload: ReportUpdate, db: Session = Depends(get_db)):
    """Update an existing report status or assignment by primary key ID."""
    return report_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete Report")
def delete_report(id: int, db: Session = Depends(get_db)):
    """Delete a single report by primary key ID."""
    return report_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Reports")
def delete_all_reports(db: Session = Depends(get_db)):
    """Bulk delete all reports."""
    return report_controller.delete_all(db)
