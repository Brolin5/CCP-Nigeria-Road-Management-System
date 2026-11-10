from sqlalchemy import Column, Integer, String, Float, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class RoadProject(Base):
    """
    Road Construction & Rehabilitation Contract Entity (Data Flow F2).
    Tracks contract progress, budget, assigned contractor, and supervisory approvals.
    """
    __tablename__ = "road_projects"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. "PRJ-2026-FCT-04"
    title = Column(String(200), nullable=False)                                # e.g. "Dualization of Abuja-Nyanya Corridor"
    description = Column(String(500), nullable=True)
    
    road_id = Column(Integer, ForeignKey("roads.id", ondelete="CASCADE"), nullable=False)
    contractor_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    
    supervising_agency = Column(String(100), default="Federal Ministry of Works", nullable=False)
    budget_naira = Column(Numeric(15, 2), nullable=True)
    
    start_date = Column(Date, nullable=True)
    expected_completion_date = Column(Date, nullable=True)
    
    # Progress & State
    current_progress_pct = Column(Float, default=0.0, nullable=False) # e.g. 45.5%
    status = Column(String(50), default="Ongoing", index=True, nullable=False) # "Not Started", "Ongoing", "Under Review", "Completed", "Abandoned"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    road = relationship("RoadSegment", back_populates="projects", foreign_keys=[road_id])
    contractor = relationship("User", back_populates="assigned_projects", foreign_keys=[contractor_id])
    milestones = relationship("ProjectMilestone", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<RoadProject(code='{self.project_code}', title='{self.title}', progress={self.current_progress_pct}%)>"
