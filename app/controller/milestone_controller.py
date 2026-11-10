from typing import List
from sqlalchemy.orm import Session
from app.service.milestone_service import milestone_service
from app.schema.milestone_schema import MilestoneResponse
from .base_controller import BaseController

class MilestoneController(BaseController):
    def __init__(self):
        super().__init__(service=milestone_service, entity_name="ProjectMilestone")

    def get_by_project_id(self, project_id: int, db: Session) -> List[MilestoneResponse]:
        return milestone_service.get_by_project_id(db, project_id)

milestone_controller = MilestoneController()
