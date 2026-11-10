from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.model.audit_log import AuditLog
from .base_repository import BaseRepository

class AuditLogRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=AuditLog,
            search_fields=["action", "entity_type", "ip_address", "old_values", "new_values"]
        )

    def get_by_entity(self, db: Session, entity_type: str, entity_id: int) -> List[Dict[str, Any]]:
        logs = db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).all()
        return [self._to_dict(l) for l in logs]

audit_log_repository = AuditLogRepository()
