from sqlalchemy.orm import Session
from app.repository.role_repository import role_repository
from app.schema.role_schema import RoleCreate, RoleUpdate, RoleResponse
from .base_service import BaseService

class RoleService(BaseService):
    def __init__(self):
        super().__init__(repository=role_repository, response_schema=RoleResponse)

    def insert(self, db: Session, payload: RoleCreate) -> RoleResponse:
        existing = role_repository.get_by_name(db, payload.name)
        if existing:
            raise ValueError(f"Role '{payload.name}' already exists.")
        return super().insert(db, payload)

role_service = RoleService()
