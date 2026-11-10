from typing import List
from sqlalchemy.orm import Session
from app.service.notification_service import notification_service
from app.schema.notification_schema import NotificationResponse
from .base_controller import BaseController

class NotificationController(BaseController):
    def __init__(self):
        super().__init__(service=notification_service, entity_name="NotificationLog")

    def get_by_recipient(self, recipient: str, db: Session) -> List[NotificationResponse]:
        return notification_service.get_by_recipient(db, recipient)

notification_controller = NotificationController()
