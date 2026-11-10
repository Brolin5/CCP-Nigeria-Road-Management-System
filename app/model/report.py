from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class RoadReport(Base):
    """
    Crowdsourced Citizen Incident & Defect Reporting Entity (Data Flow F1).
    Captures GPS coordinates, photographic proof, defect/violation category,
    and supports 100-meter duplicate report clustering.
    """
    __tablename__ = "road_reports"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. "NRMS-2026-X89J21"
    
    # "defect" (potholes, erosion) or "violation" (one-way driving, illegal parking)
    report_type = Column(String(50), index=True, nullable=False) 
    
    # Specific fault classification
    category = Column(String(100), index=True, nullable=False) 
    description = Column(Text, nullable=True)
    
    # Precise Geolocation
    latitude = Column(Float, index=True, nullable=False)
    longitude = Column(Float, index=True, nullable=False)
    location_description = Column(String(255), nullable=True)
    
    # Binary Photographic Evidence URL (Cloudinary / S3)
    photo_url = Column(String(500), nullable=False)
    
    # Severity & Triage Status
    severity = Column(String(50), default="Medium", nullable=False) # "Low", "Medium", "High", "Critical"
    status = Column(String(50), default="Pending", index=True, nullable=False) # "Pending", "Under Review", "Assigned", "Resolved", "Duplicate"
    
    # 100m Duplicate Report Clustering Support
    is_duplicate = Column(Boolean, default=False, nullable=False)
    duplicate_of_id = Column(Integer, ForeignKey("road_reports.id", ondelete="SET NULL"), nullable=True)
    
    # Foreign Key Associations
    citizen_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    road_id = Column(Integer, ForeignKey("roads.id", ondelete="SET NULL"), nullable=True)
    
    assigned_maintenance_team = Column(String(100), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    citizen = relationship("User", back_populates="reports", foreign_keys=[citizen_id])
    road = relationship("RoadSegment", back_populates="reports", foreign_keys=[road_id])
    duplicate_reports = relationship("RoadReport", foreign_keys=[duplicate_of_id])

    def __repr__(self) -> str:
        return f"<RoadReport(ticket='{self.ticket_number}', category='{self.category}', status='{self.status}')>"
