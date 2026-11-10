from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.model.project import RoadProject
from .base_repository import BaseRepository

class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=RoadProject,
            search_fields=["project_code", "title", "description", "supervising_agency", "status"]
        )

    def get_by_code(self, db: Session, project_code: str) -> Optional[Dict[str, Any]]:
        project = db.query(RoadProject).filter(RoadProject.project_code == project_code).first()
        return self._to_dict(project)

project_repository = ProjectRepository()
