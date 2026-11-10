from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    """
    User entity supporting Citizens, Contractors, Field Inspectors, and Agency Officials.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    phone_number = Column(String(25), nullable=True)  # For SMS notifications
    organization = Column(String(100), nullable=True) # e.g. FERMA, Ministry of Works, Julius Berger
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    reports = relationship("RoadReport", back_populates="citizen", foreign_keys="RoadReport.citizen_id")
    assigned_projects = relationship("RoadProject", back_populates="contractor", foreign_keys="RoadProject.contractor_id")
    inspections = relationship("Inspection", back_populates="inspector", foreign_keys="Inspection.inspector_id")

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"
