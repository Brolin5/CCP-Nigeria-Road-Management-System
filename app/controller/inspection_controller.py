from typing import List
from sqlalchemy.orm import Session
from app.service.inspection_service import inspection_service
from app.schema.inspection_schema import InspectionResponse
from .base_controller import BaseController

class InspectionController(BaseController):
    def __init__(self):
        super().__init__(service=inspection_service, entity_name="Inspection")

    def get_by_road_id(self, road_id: int, db: Session) -> List[InspectionResponse]:
        return inspection_service.get_by_road_id(db, road_id)

inspection_controller = InspectionController()
