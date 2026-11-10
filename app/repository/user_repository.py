from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.model.user import User
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=User,
            search_fields=["username", "email", "full_name", "organization", "phone_number"]
        )

    def get_by_username(self, db: Session, username: str) -> Optional[Dict[str, Any]]:
        user = db.query(User).filter(User.username == username).first()
        return self._to_dict(user)

    def get_by_email(self, db: Session, email: str) -> Optional[Dict[str, Any]]:
        user = db.query(User).filter(User.email == email).first()
        return self._to_dict(user)

user_repository = UserRepository()
