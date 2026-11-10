from typing import List
from sqlalchemy.orm import Session
from app.repository.notification_repository import notification_repository
from app.schema.notification_schema import NotificationCreate, NotificationUpdate, NotificationResponse
from .base_service import BaseService

class NotificationService(BaseService):
    def __init__(self):
        super().__init__(repository=notification_repository, response_schema=NotificationResponse)

    def get_by_recipient(self, db: Session, recipient: str) -> List[NotificationResponse]:
        notifications = notification_repository.get_by_recipient(db, recipient)
        return [NotificationResponse(**n) for n in notifications]

notification_service = NotificationService()
