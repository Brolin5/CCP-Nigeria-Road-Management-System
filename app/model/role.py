from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Role(Base):
    """
    User authorization roles:
    - 'citizen': Can report road defects and traffic violations, view tickets.
    - 'contractor': Can access assigned projects, upload milestone progress photos.
    - 'inspector': Can conduct site inspections, verify milestones, submit inspection findings.
    - 'admin': Agency officials managing the spatial dashboard, assigning crews, generating reports.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")

    def __repr__(self) -> str:
        return f"<Role(name='{self.name}')>"
