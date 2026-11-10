from typing import List
from sqlalchemy.orm import Session
from app.repository.audit_log_repository import audit_log_repository
from app.schema.audit_log_schema import AuditLogCreate, AuditLogUpdate, AuditLogResponse
from .base_service import BaseService

class AuditLogService(BaseService):
    def __init__(self):
        super().__init__(repository=audit_log_repository, response_schema=AuditLogResponse)

    def get_by_entity(self, db: Session, entity_type: str, entity_id: int) -> List[AuditLogResponse]:
        logs = audit_log_repository.get_by_entity(db, entity_type, entity_id)
        return [AuditLogResponse(**l) for l in logs]

audit_log_service = AuditLogService()
