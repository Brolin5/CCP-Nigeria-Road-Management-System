from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from app.model.report import RoadReport
from .base_repository import BaseRepository

class ReportRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_class=RoadReport,
            search_fields=["ticket_number", "category", "description", "location_description", "severity", "status"]
        )

    def get_by_ticket(self, db: Session, ticket_number: str) -> Optional[Dict[str, Any]]:
        report = db.query(RoadReport).filter(RoadReport.ticket_number == ticket_number).first()
        return self._to_dict(report)

    def find_nearby_reports(self, db: Session, lat: float, lng: float, delta: float = 0.002) -> List[Dict[str, Any]]:
        """Finds reports within ~200m bounding box to facilitate deduplication."""
        reports = db.query(RoadReport).filter(
            RoadReport.latitude.between(lat - delta, lat + delta),
            RoadReport.longitude.between(lng - delta, lng + delta),
            RoadReport.is_duplicate.is_(False)
        ).all()
        return [self._to_dict(r) for r in reports]

report_repository = ReportRepository()
