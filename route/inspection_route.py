from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.inspection_controller import inspection_controller
from app.schema.inspection_schema import InspectionCreate, InspectionUpdate, InspectionResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/inspections", tags=["Inspections"])

@router.post("/", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED, summary="Insert Inspection")
def insert_inspection(payload: InspectionCreate, db: Session = Depends(get_db)):
    """Schedule and insert a new road or project quality inspection."""
    return inspection_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[InspectionResponse], summary="Paginate Inspections")
def get_inspections_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch inspections with pagination."""
    return inspection_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[InspectionResponse], summary="Search Inspections Real-Time")
def search_inspections(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search inspections in real-time across findings summary, quality rating, or status."""
    return inspection_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/by-road/{road_id}", response_model=List[InspectionResponse], summary="Get Inspections by Road ID")
def get_inspections_by_road(road_id: int, db: Session = Depends(get_db)):
    """Fetch all inspection history records for a given road."""
    return inspection_controller.get_by_road_id(road_id, db)

@router.get("/{id}", response_model=InspectionResponse, summary="Get Inspection by ID")
def get_inspection_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single inspection by primary key ID."""
    return inspection_controller.get_by_id(id, db)

@router.put("/{id}", response_model=InspectionResponse, summary="Update Inspection")
def update_inspection(id: int, payload: InspectionUpdate, db: Session = Depends(get_db)):
    """Update inspection findings, rating, or completion status."""
    return inspection_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete Inspection")
def delete_inspection(id: int, db: Session = Depends(get_db)):
    """Delete a single inspection by primary key ID."""
    return inspection_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Inspections")
def delete_all_inspections(db: Session = Depends(get_db)):
    """Bulk delete all inspections."""
    return inspection_controller.delete_all(db)
