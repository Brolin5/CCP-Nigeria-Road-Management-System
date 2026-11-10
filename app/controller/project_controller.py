from app.service.project_service import project_service
from .base_controller import BaseController

class ProjectController(BaseController):
    def __init__(self):
        super().__init__(service=project_service, entity_name="RoadProject")

project_controller = ProjectController()
