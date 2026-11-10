from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.road_controller import road_controller
from app.schema.road_schema import RoadCreate, RoadUpdate, RoadResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/roads", tags=["Roads"])

@router.post("/", response_model=RoadResponse, status_code=status.HTTP_201_CREATED, summary="Insert Road")
def insert_road(payload: RoadCreate, db: Session = Depends(get_db)):
    """Insert a new road segment into the database."""
    return road_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[RoadResponse], summary="Paginate Roads")
def get_roads_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch roads with pagination to optimize map rendering and dashboard load times."""
    return road_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[RoadResponse], summary="Search Roads Real-Time")
def search_roads(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search roads in real-time across name, road code, state, LGA, or condition status."""
    return road_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/{id}", response_model=RoadResponse, summary="Get Road by ID")
def get_road_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single road by primary key ID."""
    return road_controller.get_by_id(id, db)

@router.put("/{id}", response_model=RoadResponse, summary="Update Road")
def update_road(id: int, payload: RoadUpdate, db: Session = Depends(get_db)):
    """Update an existing road by primary key ID."""
    return road_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete Road")
def delete_road(id: int, db: Session = Depends(get_db)):
    """Delete a single road by primary key ID."""
    return road_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Roads")
def delete_all_roads(db: Session = Depends(get_db)):
    """Bulk delete all roads."""
    return road_controller.delete_all(db)
