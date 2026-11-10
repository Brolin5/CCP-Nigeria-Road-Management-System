from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.model.inspection import Inspection
from .base_repository import BaseRepository

class InspectionRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=Inspection,
            search_fields=["status", "findings_summary", "quality_rating"]
        )

    def get_by_road_id(self, db: Session, road_id: int) -> List[Dict[str, Any]]:
        inspections = db.query(Inspection).filter(Inspection.road_id == road_id).all()
        return [self._to_dict(i) for i in inspections]

inspection_repository = InspectionRepository()
