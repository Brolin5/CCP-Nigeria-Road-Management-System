from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class RoadSegment(Base):
    """
    Road inventory entity representing Federal, State, and Local Government road assets.
    Tracks condition status and last inspection date for the automated 30-day alert engine.
    """
    __tablename__ = "roads"

    id = Column(Integer, primary_key=True, index=True)
    road_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. "FED-A234-ABJ"
    name = Column(String(150), nullable=False)                             # e.g. "Abuja-Keffi Dual Carriageway"
    classification = Column(String(50), nullable=False, default="Federal")  # Federal, State, Local
    state = Column(String(50), index=True, nullable=False)                 # e.g. "FCT", "Lagos", "Kano"
    lga = Column(String(100), nullable=True)                               # Local Government Area
    length_km = Column(Float, nullable=True)
    start_latitude = Column(Float, nullable=True)
    start_longitude = Column(Float, nullable=True)
    end_latitude = Column(Float, nullable=True)
    end_longitude = Column(Float, nullable=True)
    condition_status = Column(String(50), default="Fair", nullable=False)  # "Good", "Fair", "Poor", "Critical"
    
    # 30-Day Automated Inspection Alert Tracking
    last_inspected_at = Column(DateTime, nullable=True)
    is_inspection_overdue = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    reports = relationship("RoadReport", back_populates="road", foreign_keys="RoadReport.road_id")
    projects = relationship("RoadProject", back_populates="road", foreign_keys="RoadProject.road_id")
    inspections = relationship("Inspection", back_populates="road", foreign_keys="Inspection.road_id")

    def __repr__(self) -> str:
        return f"<RoadSegment(code='{self.road_code}', name='{self.name}', condition='{self.condition_status}')>"
