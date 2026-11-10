from typing import Any, Dict, Optional, Type
from sqlalchemy.orm import Session
from app.repository.base_repository import BaseRepository
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

class BaseService:
    """
    Business Logic Layer (Service Layer).
    Implements business rules, validation, and domain operations.
    CRITICAL ARCHITECTURAL RULE: Does NOT import or manipulate SQLAlchemy Models directly.
    Communicates exclusively with the Repository Layer and Schema/DTOs.
    """
    def __init__(self, repository: BaseRepository, response_schema: Type[Any]):
        self.repository = repository
        self.response_schema = response_schema

    def insert(self, db: Session, payload: Any) -> Any:
        """Insert/Create a new domain record with business validation."""
        data_dict = payload.model_dump() if hasattr(payload, "model_dump") else dict(payload)
        created_dict = self.repository.insert(db, data_dict)
        return self.response_schema(**created_dict)

    def get_by_id(self, db: Session, entity_id: int) -> Optional[Any]:
        """Fetch a single record by primary key."""
        entity_dict = self.repository.get_by_id(db, entity_id)
        if not entity_dict:
            return None
        return self.response_schema(**entity_dict)

    def update(self, db: Session, entity_id: int, payload: Any) -> Optional[Any]:
        """Update an existing record by primary key."""
        data_dict = payload.model_dump(exclude_unset=True) if hasattr(payload, "model_dump") else dict(payload)
        updated_dict = self.repository.update(db, entity_id, data_dict)
        if not updated_dict:
            return None
        return self.response_schema(**updated_dict)

    def delete(self, db: Session, entity_id: int) -> bool:
        """Delete an existing record by primary key."""
        return self.repository.delete(db, entity_id)

    def delete_all(self, db: Session) -> DeleteAllResponse:
        """Bulk delete all records in the table."""
        count = self.repository.delete_all(db)
        return DeleteAllResponse(
            success=True,
            deleted_count=count,
            message=f"Successfully deleted {count} records."
        )

    def pagination(self, db: Session, page: int = 1, limit: int = 10) -> PaginatedResponse:
        """Fetch records with pagination."""
        result = self.repository.get_paginated(db, page=page, limit=limit)
        items = [self.response_schema(**item) for item in result["items"]]
        return PaginatedResponse(
            total=result["total"],
            page=result["page"],
            limit=result["limit"],
            total_pages=result["total_pages"],
            items=items
        )

    def search(self, db: Session, query: str, page: int = 1, limit: int = 10) -> PaginatedResponse:
        """Real-time text search with pagination."""
        result = self.repository.search(db, search_query=query, page=page, limit=limit)
        items = [self.response_schema(**item) for item in result["items"]]
        return PaginatedResponse(
            total=result["total"],
            page=result["page"],
            limit=result["limit"],
            total_pages=result["total_pages"],
            items=items
        )
