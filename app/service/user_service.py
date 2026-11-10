import hashlib
from typing import Optional
from sqlalchemy.orm import Session
from app.repository.user_repository import user_repository
from app.schema.user_schema import UserCreate, UserUpdate, UserResponse
from .base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__(repository=user_repository, response_schema=UserResponse)

    @staticmethod
    def _hash_password(raw_password: str) -> str:
        return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()

    def insert(self, db: Session, payload: UserCreate) -> UserResponse:
        # Check uniqueness
        if user_repository.get_by_username(db, payload.username):
            raise ValueError(f"Username '{payload.username}' is already taken.")
        if user_repository.get_by_email(db, payload.email):
            raise ValueError(f"Email '{payload.email}' is already registered.")

        data = payload.model_dump()
        raw_pw = data.pop("password")
        data["hashed_password"] = self._hash_password(raw_pw)

        created_dict = self.repository.insert(db, data)
        return UserResponse(**created_dict)

    def update(self, db: Session, user_id: int, payload: UserUpdate) -> Optional[UserResponse]:
        data = payload.model_dump(exclude_unset=True)
        if "password" in data and data["password"]:
            raw_pw = data.pop("password")
            data["hashed_password"] = self._hash_password(raw_pw)
        updated_dict = self.repository.update(db, user_id, data)
        if not updated_dict:
            return None
        return UserResponse(**updated_dict)

user_service = UserService()
