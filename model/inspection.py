from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Inspection(Base):
    """
    Inspection Scheduling & Quality Assurance Entity (Data Flow F3).
    Tracks field audits on road segments and ongoing contractor project sites.
    """
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    road_id = Column(Integer, ForeignKey("roads.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(Integer, ForeignKey("road_projects.id", ondelete="SET NULL"), nullable=True)
    inspector_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    scheduled_date = Column(Date, nullable=False)
    conducted_date = Column(Date, nullable=True)
    status = Column(String(50), default="Scheduled", index=True, nullable=False) # "Scheduled", "Completed", "Overdue", "Cancelled"
    
    findings_summary = Column(Text, nullable=True)
    quality_rating = Column(String(50), nullable=True) # "Satisfactory", "Minor Defects", "Critical Non-Compliance"
    evidence_photos_json = Column(Text, nullable=True)  # JSON list of inspection photos
    
    # 30-Day Automated Alert Dispatch Tracking
    alert_dispatched = Column(Boolean, default=False, nullable=False)
    alert_dispatched_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    road = relationship("RoadSegment", back_populates="inspections", foreign_keys=[road_id])
    inspector = relationship("User", back_populates="inspections", foreign_keys=[inspector_id])

    def __repr__(self) -> str:
        return f"<Inspection(id={self.id}, road_id={self.road_id}, status='{self.status}')>"
