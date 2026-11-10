from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.audit_log_controller import audit_log_controller
from app.schema.audit_log_schema import AuditLogCreate, AuditLogUpdate, AuditLogResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.post("/", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED, summary="Insert Audit Log")
def insert_audit_log(payload: AuditLogCreate, db: Session = Depends(get_db)):
    """Insert a forensic audit trail entry."""
    return audit_log_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[AuditLogResponse], summary="Paginate Audit Logs")
def get_audit_logs_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch audit logs with pagination to review forensic history."""
    return audit_log_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[AuditLogResponse], summary="Search Audit Logs Real-Time")
def search_audit_logs(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search audit logs in real-time across action, entity type, IP address, or diff values."""
    return audit_log_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/by-entity", response_model=List[AuditLogResponse], summary="Get Audit Logs by Entity")
def get_audit_logs_by_entity(
    entity_type: str = Query(..., description="e.g. RoadReport, RoadProject"),
    entity_id: int = Query(..., description="Entity ID"),
    db: Session = Depends(get_db)
):
    """Fetch forensic audit logs for a specific entity."""
    return audit_log_controller.get_by_entity(entity_type, entity_id, db)

@router.get("/{id}", response_model=AuditLogResponse, summary="Get Audit Log by ID")
def get_audit_log_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single audit log by primary key ID."""
    return audit_log_controller.get_by_id(id, db)

@router.put("/{id}", response_model=AuditLogResponse, summary="Update Audit Log")
def update_audit_log(id: int, payload: AuditLogUpdate, db: Session = Depends(get_db)):
    """Update an audit log entry."""
    return audit_log_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete Audit Log")
def delete_audit_log(id: int, db: Session = Depends(get_db)):
    """Delete an audit log entry by primary key ID."""
    return audit_log_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Audit Logs")
def delete_all_audit_logs(db: Session = Depends(get_db)):
    """Bulk delete all audit logs."""
    return audit_log_controller.delete_all(db)
