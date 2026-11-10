from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.role_controller import role_controller
from app.schema.role_schema import RoleCreate, RoleUpdate, RoleResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED, summary="Insert Role")
def insert_role(payload: RoleCreate, db: Session = Depends(get_db)):
    """Insert a new role into the database."""
    return role_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[RoleResponse], summary="Paginate Roles")
def get_roles_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch roles with pagination."""
    return role_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[RoleResponse], summary="Search Roles Real-Time")
def search_roles(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search roles in real-time across role name and description."""
    return role_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/{id}", response_model=RoleResponse, summary="Get Role by ID")
def get_role_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single role by primary key ID."""
    return role_controller.get_by_id(id, db)

@router.put("/{id}", response_model=RoleResponse, summary="Update Role")
def update_role(id: int, payload: RoleUpdate, db: Session = Depends(get_db)):
    """Update an existing role by primary key ID."""
    return role_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete Role")
def delete_role(id: int, db: Session = Depends(get_db)):
    """Delete a single role by primary key ID."""
    return role_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Roles")
def delete_all_roles(db: Session = Depends(get_db)):
    """Bulk delete all roles."""
    return role_controller.delete_all(db)
