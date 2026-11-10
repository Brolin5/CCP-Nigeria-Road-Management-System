from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class AuditLog(Base):
    """
    Comprehensive System Audit Trail Entity.
    Guarantees non-repudiation, accountability, and traceability by logging
    all critical administrative mutations, status transitions, and data changes.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Action classification: REPORT_SUBMITTED, STATUS_CHANGED, MILESTONE_APPROVED, etc.
    action = Column(String(100), index=True, nullable=False)
    
    # Affected Domain Entity (e.g. 'RoadReport', 'ProjectMilestone', 'RoadSegment')
    entity_type = Column(String(50), index=True, nullable=False)
    entity_id = Column(Integer, nullable=True)
    
    # State change snapshots (JSON format)
    old_values = Column(Text, nullable=True)
    new_values = Column(Text, nullable=True)
    
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self) -> str:
        return f"<AuditLog(action='{self.action}', entity='{self.entity_type}', id={self.entity_id})>"
