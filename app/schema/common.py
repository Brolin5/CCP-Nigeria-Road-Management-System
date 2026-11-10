from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number, starting from 1")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page (max 100)")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int = Field(..., description="Total number of items matching query")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total available pages")
    items: List[T] = Field(..., description="List of items for current page")

class DeleteAllResponse(BaseModel):
    success: bool = True
    deleted_count: int
    message: str

class MessageResponse(BaseModel):
    success: bool = True
    message: str
