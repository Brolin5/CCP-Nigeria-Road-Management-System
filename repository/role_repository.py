from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.model.role import Role
from .base_repository import BaseRepository

class RoleRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=Role,
            search_fields=["name", "description"]
        )

    def get_by_name(self, db: Session, name: str) -> Optional[Dict[str, Any]]:
        role = db.query(Role).filter(Role.name == name).first()
        return self._to_dict(role)

role_repository = RoleRepository()
