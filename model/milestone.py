from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class ProjectMilestone(Base):
    """
    Contractor Milestone Progress & Quality Assurance Entity (Data Flow F2).
    Requires timestamped on-site photographic evidence before payment sign-off.
    """
    __tablename__ = "project_milestones"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("road_projects.id", ondelete="CASCADE"), nullable=False)
    
    milestone_name = Column(String(150), nullable=False) # e.g. "Culvert Casting", "Asphalt Binder Course"
    milestone_order = Column(Integer, default=1, nullable=False)
    percentage_weight = Column(Float, default=0.0, nullable=False) # e.g. 20% of total project
    progress_pct_achieved = Column(Float, default=0.0, nullable=False)
    
    # Photographic Evidence of Milestone Stage (Cloudinary/S3 link)
    photo_evidence_url = Column(String(500), nullable=True)
    contractor_notes = Column(Text, nullable=True)
    
    # Milestone Inspection Clearance Status
    status = Column(String(50), default="Pending", index=True, nullable=False) # "Pending", "Pending Inspection", "Approved", "Rejected"
    
    submitted_at = Column(DateTime, nullable=True)
    inspected_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    project = relationship("RoadProject", back_populates="milestones", foreign_keys=[project_id])

    def __repr__(self) -> str:
        return f"<ProjectMilestone(name='{self.milestone_name}', status='{self.status}')>"
