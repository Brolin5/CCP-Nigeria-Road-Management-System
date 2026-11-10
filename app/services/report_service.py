import math
import secrets
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.config import settings
from app.model import RoadReport, RoadSegment
from app.schemas.report_schema import ReportCreate, ReportStatusUpdate

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two GPS points in meters using Haversine formula.
    """
    R = 6371000.0  # Earth's radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

class ReportService:
    @staticmethod
    def generate_ticket_number() -> str:
        year = datetime.now().year
        suffix = secrets.token_hex(3).upper()
        return f"NRMS-{year}-{suffix}"

    @classmethod
    def create_report(cls, db: Session, report_in: ReportCreate) -> RoadReport:
        # 1. Check for duplicate reports within DUPLICATE_RADIUS_METERS (100m)
        radius_m = settings.DUPLICATE_RADIUS_METERS
        recent_reports = db.query(RoadReport).filter(
            RoadReport.category == report_in.category,
            RoadReport.status.in_(["Pending", "Under Review", "Assigned"])
        ).all()

        is_duplicate = False
        duplicate_of_id = None

        for existing in recent_reports:
            dist = haversine_distance_meters(
                report_in.latitude, report_in.longitude,
                existing.latitude, existing.longitude
            )
            if dist <= radius_m:
                is_duplicate = True
                duplicate_of_id = existing.id
                break

        # 2. Assign unique tracking ticket
        ticket = cls.generate_ticket_number()

        report = RoadReport(
            ticket_number=ticket,
            report_type=report_in.report_type.lower(),
            category=report_in.category,
            description=report_in.description,
            latitude=report_in.latitude,
            longitude=report_in.longitude,
            location_description=report_in.location_description,
            photo_url=report_in.photo_url,
            severity=report_in.severity,
            status="Duplicate" if is_duplicate else "Pending",
            is_duplicate=is_duplicate,
            duplicate_of_id=duplicate_of_id,
            citizen_id=report_in.citizen_id,
            road_id=report_in.road_id
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_reports(
        db: Session,
        report_type: Optional[str] = None,
        category: Optional[str] = None,
        status_filter: Optional[str] = None,
        road_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[RoadReport]:
        query = db.query(RoadReport)
        if report_type:
            query = query.filter(RoadReport.report_type == report_type.lower())
        if category:
            query = query.filter(RoadReport.category == category)
        if status_filter:
            query = query.filter(RoadReport.status == status_filter)
        if road_id:
            query = query.filter(RoadReport.road_id == road_id)
        return query.order_by(RoadReport.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_report_by_ticket(db: Session, ticket_number: str) -> RoadReport:
        report = db.query(RoadReport).filter(RoadReport.ticket_number == ticket_number).first()
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report with ticket number {ticket_number} not found."
            )
        return report

    @staticmethod
    def update_report_status(db: Session, report_id: int, update_in: ReportStatusUpdate) -> RoadReport:
        report = db.query(RoadReport).filter(RoadReport.id == report_id).first()
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report #{report_id} not found."
            )
        report.status = update_in.status
        if update_in.assigned_maintenance_team:
            report.assigned_maintenance_team = update_in.assigned_maintenance_team
        if update_in.status == "Resolved":
            report.resolved_at = datetime.utcnow()
        db.commit()
        db.refresh(report)
        return report
