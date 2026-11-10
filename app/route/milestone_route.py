from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.milestone_controller import milestone_controller
from app.schema.milestone_schema import MilestoneCreate, MilestoneUpdate, MilestoneResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/milestones", tags=["Milestones"])

@router.post("/", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED, summary="Insert Milestone")
def insert_milestone(payload: MilestoneCreate, db: Session = Depends(get_db)):
    """Insert a new staged project milestone."""
    return milestone_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[MilestoneResponse], summary="Paginate Milestones")
def get_milestones_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch milestones with pagination."""
    return milestone_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[MilestoneResponse], summary="Search Milestones Real-Time")
def search_milestones(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search milestones in real-time across milestone name, contractor notes, or status."""
    return milestone_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/by-project/{project_id}", response_model=List[MilestoneResponse], summary="Get Milestones by Project ID")
def get_milestones_by_project(project_id: int, db: Session = Depends(get_db)):
    """Fetch all sequential milestones for a specific project."""
    return milestone_controller.get_by_project_id(project_id, db)

@router.get("/{id}", response_model=MilestoneResponse, summary="Get Milestone by ID")
def get_milestone_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single milestone by primary key ID."""
    return milestone_controller.get_by_id(id, db)

@router.put("/{id}", response_model=MilestoneResponse, summary="Update Milestone")
def update_milestone(id: int, payload: MilestoneUpdate, db: Session = Depends(get_db)):
    """Update milestone progress percentage or inspection status."""
    return milestone_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete Milestone")
def delete_milestone(id: int, db: Session = Depends(get_db)):
    """Delete a single milestone by primary key ID."""
    return milestone_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Milestones")
def delete_all_milestones(db: Session = Depends(get_db)):
    """Bulk delete all milestones."""
    return milestone_controller.delete_all(db)
