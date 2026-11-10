from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.model.road import RoadSegment
from .base_repository import BaseRepository

class RoadRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=RoadSegment,
            search_fields=["road_code", "name", "classification", "state", "lga", "condition_status"]
        )

    def get_by_code(self, db: Session, road_code: str) -> Optional[Dict[str, Any]]:
        road = db.query(RoadSegment).filter(RoadSegment.road_code == road_code).first()
        return self._to_dict(road)

road_repository = RoadRepository()
