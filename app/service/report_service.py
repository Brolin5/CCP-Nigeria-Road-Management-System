import uuid
from sqlalchemy.orm import Session
from app.repository.report_repository import report_repository
from app.schema.report_schema import ReportCreate, ReportUpdate, ReportResponse
from .base_service import BaseService

class ReportService(BaseService):
    def __init__(self):
        super().__init__(repository=report_repository, response_schema=ReportResponse)

    def insert(self, db: Session, payload: ReportCreate) -> ReportResponse:
        data = payload.model_dump()
        
        # Anti-Spoofing: Geofence Validation for Nigerian Territorial Bounds
        lat = data.get("latitude")
        lng = data.get("longitude")
        if lat is not None and lng is not None:
            if not (4.0 <= lat <= 14.0 and 2.5 <= lng <= 15.0):
                raise ValueError(
                    f"Anti-Spoofing Error: GPS coordinates ({lat}, {lng}) fall outside "
                    f"Nigerian territory [Lat: 4.0°-14.0°N, Lng: 2.5°-15.0°E]. Spoofed or invalid location rejected."
                )

        if not data.get("ticket_number"):
            short_id = uuid.uuid4().hex[:6].upper()
            data["ticket_number"] = f"NRMS-2026-{short_id}"

        # Automatic Duplicate Check (Real-time Spatial Deduplication)
        nearby = report_repository.find_nearby_reports(db, data["latitude"], data["longitude"])
        if nearby:
            data["is_duplicate"] = True
            data["duplicate_of_id"] = nearby[0]["id"]
            data["status"] = "Duplicate"

        created_dict = self.repository.insert(db, data)
        return ReportResponse(**created_dict)

report_service = ReportService()
