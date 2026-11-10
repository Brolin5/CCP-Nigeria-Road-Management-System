from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.model.milestone import ProjectMilestone
from .base_repository import BaseRepository

class MilestoneRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=ProjectMilestone,
            search_fields=["milestone_name", "contractor_notes", "status"]
        )

    def get_by_project_id(self, db: Session, project_id: int) -> List[Dict[str, Any]]:
        milestones = db.query(ProjectMilestone).filter(ProjectMilestone.project_id == project_id).order_by(ProjectMilestone.milestone_order).all()
        return [self._to_dict(m) for m in milestones]

milestone_repository = MilestoneRepository()
