from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.model.notification import NotificationLog
from .base_repository import BaseRepository

class NotificationRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=NotificationLog,
            search_fields=["recipient", "subject", "message", "channel", "status"]
        )

    def get_by_recipient(self, db: Session, recipient: str) -> List[Dict[str, Any]]:
        notifications = db.query(NotificationLog).filter(NotificationLog.recipient == recipient).all()
        return [self._to_dict(n) for n in notifications]

notification_repository = NotificationRepository()
