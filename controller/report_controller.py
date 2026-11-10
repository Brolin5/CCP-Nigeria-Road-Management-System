from app.service.report_service import report_service
from .base_controller import BaseController

class ReportController(BaseController):
    def __init__(self):
        super().__init__(service=report_service, entity_name="RoadReport")

report_controller = ReportController()
