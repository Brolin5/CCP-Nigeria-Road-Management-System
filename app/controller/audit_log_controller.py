from typing import List
from sqlalchemy.orm import Session
from app.service.audit_log_service import audit_log_service
from app.schema.audit_log_schema import AuditLogResponse
from .base_controller import BaseController

class AuditLogController(BaseController):
    def __init__(self):
        super().__init__(service=audit_log_service, entity_name="AuditLog")

    def get_by_entity(self, entity_type: str, entity_id: int, db: Session) -> List[AuditLogResponse]:
        return audit_log_service.get_by_entity(db, entity_type, entity_id)

audit_log_controller = AuditLogController()
