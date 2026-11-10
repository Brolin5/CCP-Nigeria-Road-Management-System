from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.notification_controller import notification_controller
from app.schema.notification_schema import NotificationCreate, NotificationUpdate, NotificationResponse
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED, summary="Insert Notification")
def insert_notification(payload: NotificationCreate, db: Session = Depends(get_db)):
    """Insert and log an SMS or Email notification."""
    return notification_controller.insert(payload, db)

@router.get("/", response_model=PaginatedResponse[NotificationResponse], summary="Paginate Notifications")
def get_notifications_paginated(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Fetch logged notifications with pagination."""
    return notification_controller.pagination(page=page, limit=limit, db=db)

@router.get("/search", response_model=PaginatedResponse[NotificationResponse], summary="Search Notifications Real-Time")
def search_notifications(
    q: str = Query(..., min_length=1, description="Real-time search text query"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search notifications in real-time across recipient, subject, channel, or message body."""
    return notification_controller.search(query=q, page=page, limit=limit, db=db)

@router.get("/by-recipient", response_model=List[NotificationResponse], summary="Get Notifications by Recipient")
def get_notifications_by_recipient(recipient: str = Query(..., description="Phone or Email"), db: Session = Depends(get_db)):
    """Fetch all notification logs sent to a specific recipient phone or email."""
    return notification_controller.get_by_recipient(recipient, db)

@router.get("/{id}", response_model=NotificationResponse, summary="Get Notification by ID")
def get_notification_by_id(id: int, db: Session = Depends(get_db)):
    """Fetch a single notification log by primary key ID."""
    return notification_controller.get_by_id(id, db)

@router.put("/{id}", response_model=NotificationResponse, summary="Update Notification")
def update_notification(id: int, payload: NotificationUpdate, db: Session = Depends(get_db)):
    """Update notification status or details."""
    return notification_controller.update(id, payload, db)

@router.delete("/{id}", response_model=MessageResponse, summary="Delete Notification")
def delete_notification(id: int, db: Session = Depends(get_db)):
    """Delete a single notification log by primary key ID."""
    return notification_controller.delete(id, db)

@router.delete("/", response_model=DeleteAllResponse, summary="Delete All Notifications")
def delete_all_notifications(db: Session = Depends(get_db)):
    """Bulk delete all notification logs."""
    return notification_controller.delete_all(db)
