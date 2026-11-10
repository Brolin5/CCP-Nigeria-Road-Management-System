from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.service.base_service import BaseService
from app.schema.common import PaginatedResponse, DeleteAllResponse, MessageResponse

class BaseController:
    """
    Controller Layer (HTTP Communication Processing).
    Processes incoming HTTP calls, validates request flows, orchestrates Service calls,
    handles domain exceptions, and formats HTTP response codes.
    CRITICAL ARCHITECTURAL RULE: Does NOT import or manipulate SQLAlchemy Models directly.
    """
    def __init__(self, service: BaseService, entity_name: str = "Record"):
        self.service = service
        self.entity_name = entity_name

    def insert(self, payload: Any, db: Session) -> Any:
        """Processes insert HTTP call."""
        try:
            return self.service.insert(db, payload)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to insert {self.entity_name}: {str(e)}")

    def get_by_id(self, entity_id: int, db: Session) -> Any:
        """Processes get by id HTTP call."""
        record = self.service.get_by_id(db, entity_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.entity_name} with id {entity_id} not found.")
        return record

    def update(self, entity_id: int, payload: Any, db: Session) -> Any:
        """Processes update HTTP call."""
        try:
            record = self.service.update(db, entity_id, payload)
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.entity_name} with id {entity_id} not found.")
            return record
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update {self.entity_name}: {str(e)}")

    def delete(self, entity_id: int, db: Session) -> MessageResponse:
        """Processes single delete HTTP call."""
        success = self.service.delete(db, entity_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.entity_name} with id {entity_id} not found.")
        return MessageResponse(success=True, message=f"{self.entity_name} with id {entity_id} deleted successfully.")

    def delete_all(self, db: Session) -> DeleteAllResponse:
        """Processes delete-all / bulk-delete HTTP call."""
        try:
            return self.service.delete_all(db)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete all {self.entity_name}s: {str(e)}")

    def pagination(self, page: int, limit: int, db: Session) -> PaginatedResponse:
        """Processes pagination HTTP call to optimize page delivery."""
        try:
            return self.service.pagination(db, page=page, limit=limit)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to paginate {self.entity_name}s: {str(e)}")

    def search(self, query: str, page: int, limit: int, db: Session) -> PaginatedResponse:
        """Processes real-time search HTTP call with pagination."""
        try:
            return self.service.search(db, query=query, page=page, limit=limit)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to search {self.entity_name}s: {str(e)}")
