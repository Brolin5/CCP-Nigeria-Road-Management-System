from sqlalchemy.orm import Session
from app.repository.road_repository import road_repository
from app.schema.road_schema import RoadCreate, RoadUpdate, RoadResponse
from .base_service import BaseService

class RoadService(BaseService):
    def __init__(self):
        super().__init__(repository=road_repository, response_schema=RoadResponse)

    def insert(self, db: Session, payload: RoadCreate) -> RoadResponse:
        existing = road_repository.get_by_code(db, payload.road_code)
        if existing:
            raise ValueError(f"Road code '{payload.road_code}' already exists.")
        return super().insert(db, payload)

road_service = RoadService()
