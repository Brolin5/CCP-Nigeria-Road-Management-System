from typing import Any, Dict, List, Optional, Type
from math import ceil
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

class BaseRepository:
    """
    Data Access Layer (Repository Pattern).
    The ONLY layer that interacts directly with SQLAlchemy Models.
    Converts database models to clean dictionaries/DTOs before returning to the Service Layer.
    """
    def __init__(self, model_class: Type[Any], search_fields: Optional[List[str]] = None):
        self.model_class = model_class
        self.search_fields = search_fields or []

    def _to_dict(self, instance: Any) -> Optional[Dict[str, Any]]:
        """Converts an ORM model instance into a plain dictionary to prevent leaking Models."""
        if instance is None:
            return None
        return {col.name: getattr(instance, col.name) for col in instance.__table__.columns}

    def insert(self, db: Session, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new entity record into the database."""
        instance = self.model_class(**data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return self._to_dict(instance)

    def get_by_id(self, db: Session, entity_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single record by its primary key ID."""
        instance = db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        return self._to_dict(instance)

    def update(self, db: Session, entity_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing record by its primary key ID."""
        instance = db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        if not instance:
            return None
        for key, value in data.items():
            if hasattr(instance, key) and value is not None:
                setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
        return self._to_dict(instance)

    def delete(self, db: Session, entity_id: int) -> bool:
        """Delete a single record by its primary key ID."""
        instance = db.query(self.model_class).filter(self.model_class.id == entity_id).first()
        if not instance:
            return False
        db.delete(instance)
        db.commit()
        return True

    def delete_all(self, db: Session) -> int:
        """Bulk delete all records in the table."""
        deleted_count = db.query(self.model_class).delete()
        db.commit()
        return deleted_count

    def get_paginated(self, db: Session, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Fetch records with pagination to optimize memory and rendering."""
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10

        query = db.query(self.model_class)
        total = query.count()
        total_pages = ceil(total / limit) if total > 0 else 1

        instances = query.order_by(desc(self.model_class.id)).offset((page - 1) * limit).limit(limit).all()
        items = [self._to_dict(inst) for inst in instances]

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "items": items
        }

    def search(self, db: Session, search_query: str, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Real-time multi-column search with pagination."""
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10

        query = db.query(self.model_class)

        if search_query and self.search_fields:
            filters = []
            for field in self.search_fields:
                if hasattr(self.model_class, field):
                    column_attr = getattr(self.model_class, field)
                    filters.append(column_attr.ilike(f"%{search_query}%"))
            if filters:
                query = query.filter(or_(*filters))

        total = query.count()
        total_pages = ceil(total / limit) if total > 0 else 1

        instances = query.order_by(desc(self.model_class.id)).offset((page - 1) * limit).limit(limit).all()
        items = [self._to_dict(inst) for inst in instances]

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "items": items
        }
