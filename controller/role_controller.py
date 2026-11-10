from app.service.role_service import role_service
from .base_controller import BaseController

class RoleController(BaseController):
    def __init__(self):
        super().__init__(service=role_service, entity_name="Role")

role_controller = RoleController()
