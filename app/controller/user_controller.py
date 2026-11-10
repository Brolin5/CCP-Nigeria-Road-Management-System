from app.service.user_service import user_service
from .base_controller import BaseController

class UserController(BaseController):
    def __init__(self):
        super().__init__(service=user_service, entity_name="User")

user_controller = UserController()
