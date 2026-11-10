from app.service.road_service import road_service
from .base_controller import BaseController

class RoadController(BaseController):
    def __init__(self):
        super().__init__(service=road_service, entity_name="RoadSegment")

road_controller = RoadController()
