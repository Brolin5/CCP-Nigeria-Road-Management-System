from typing import List
from sqlalchemy.orm import Session
from app.repository.inspection_repository import inspection_repository
from app.schema.inspection_schema import InspectionCreate, InspectionUpdate, InspectionResponse
from .base_service import BaseService

class InspectionService(BaseService):
    def __init__(self):
        super().__init__(repository=inspection_repository, response_schema=InspectionResponse)

    def get_by_road_id(self, db: Session, road_id: int) -> List[InspectionResponse]:
        inspections = inspection_repository.get_by_road_id(db, road_id)
        return [InspectionResponse(**i) for i in inspections]

inspection_service = InspectionService()
