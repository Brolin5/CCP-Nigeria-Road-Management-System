from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user_controller import user_controller
from app.schema.user_schema import UserCreate, UserUpdate, UserResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Insert User")
def insert_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Insert a new user into the database."""
    return user_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[UserResponse], summary="Paginate Users")
def get_users_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch users with pagination to optimize performance."""
    return user_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[UserResponse], summary="Search Users Real-Time")
def search_users(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search users in real-time across username, email, full name, or organization."""
    return user_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/{id}", response_model=UserResponse, summary="Get User by ID")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single user by primary key ID."""
    return user_controller.get_by_id(id, db)

@router.put("/{id}", response_model=UserResponse, summary="Update User")
def update_user(id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    """Update an existing user by primary key ID."""
    return user_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete User")
def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete a single user by primary key ID."""
    return user_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Users")
def delete_all_users(db: Session = Depends(get_db)):
    """Bulk delete all users."""
    return user_controller.delete_all(db)
