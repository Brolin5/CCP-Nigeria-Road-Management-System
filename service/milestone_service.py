from typing import List
from sqlalchemy.orm import Session
from app.repository.milestone_repository import milestone_repository
from app.schema.milestone_schema import MilestoneCreate, MilestoneUpdate, MilestoneResponse
from .base_service import BaseService

class MilestoneService(BaseService):
    def __init__(self):
        super().__init__(repository=milestone_repository, response_schema=MilestoneResponse)

    def get_by_project_id(self, db: Session, project_id: int) -> List[MilestoneResponse]:
        milestones = milestone_repository.get_by_project_id(db, project_id)
        return [MilestoneResponse(**m) for m in milestones]

milestone_service = MilestoneService()
