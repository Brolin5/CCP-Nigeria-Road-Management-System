from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.project_controller import project_controller
from app.schema.project_schema import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, summary="Insert Project")
def insert_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    """Insert a new contractor highway rehabilitation project."""
    return project_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[ProjectResponse], summary="Paginate Projects")
def get_projects_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch road projects with pagination."""
    return project_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[ProjectResponse], summary="Search Projects Real-Time")
def search_projects(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search projects in real-time across project code, title, description, or supervising agency."""
    return project_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/{id}", response_model=ProjectResponse, summary="Get Project by ID")
def get_project_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single project by primary key ID."""
    return project_controller.get_by_id(id, db)

@router.put("/{id}", response_model=ProjectResponse, summary="Update Project")
def update_project(id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    """Update an existing project by primary key ID."""
    return project_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete Project")
def delete_project(id: int, db: Session = Depends(get_db)):
    """Delete a single project by primary key ID."""
    return project_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Projects")
def delete_all_projects(db: Session = Depends(get_db)):
    """Bulk delete all projects."""
    return project_controller.delete_all(db)
