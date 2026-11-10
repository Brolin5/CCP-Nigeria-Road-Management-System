from sqlalchemy.orm import Session
from app.repository.project_repository import project_repository
from app.schema.project_schema import ProjectCreate, ProjectUpdate, ProjectResponse
from .base_service import BaseService

class ProjectService(BaseService):
    def __init__(self):
        super().__init__(repository=project_repository, response_schema=ProjectResponse)

    def insert(self, db: Session, payload: ProjectCreate) -> ProjectResponse:
        existing = project_repository.get_by_code(db, payload.project_code)
        if existing:
            raise ValueError(f"Project code '{payload.project_code}' already exists.")
        return super().insert(db, payload)

project_service = ProjectService()
