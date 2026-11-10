from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.config import settings
from app.model import RoadSegment, Inspection, NotificationLog
from app.schemas.inspection_schema import InspectionCreate, InspectionComplete

class InspectionService:
    @staticmethod
    def schedule_inspection(db: Session, inspection_in: InspectionCreate) -> Inspection:
        road = db.query(RoadSegment).filter(RoadSegment.id == inspection_in.road_id).first()
        if not road:
            raise HTTPException(status_code=404, detail=f"Road segment #{inspection_in.road_id} not found.")

        inspection = Inspection(
            road_id=inspection_in.road_id,
            project_id=inspection_in.project_id,
            inspector_id=inspection_in.inspector_id,
            scheduled_date=inspection_in.scheduled_date,
            status="Scheduled"
        )
        db.add(inspection)
        db.commit()
        db.refresh(inspection)
        return inspection

    @staticmethod
    def complete_inspection(db: Session, inspection_id: int, complete_in: InspectionComplete) -> Inspection:
        inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
        if not inspection:
            raise HTTPException(status_code=404, detail=f"Inspection #{inspection_id} not found.")

        inspection.conducted_date = complete_in.conducted_date
        inspection.findings_summary = complete_in.findings_summary
        inspection.quality_rating = complete_in.quality_rating
        inspection.evidence_photos_json = complete_in.evidence_photos_json
        inspection.status = "Completed"

        # Update parent road segment's last_inspected_at
        road = db.query(RoadSegment).filter(RoadSegment.id == inspection.road_id).first()
        if road:
            road.last_inspected_at = datetime.combine(complete_in.conducted_date, datetime.min.time())
            road.is_inspection_overdue = False

        db.commit()
        db.refresh(inspection)
        return inspection

    @staticmethod
    def check_and_trigger_overdue_alerts(db: Session) -> Dict[str, Any]:
        """
        The Automated Inspection Alert Engine (Data Flow F3):
        Scans all roads where last_inspected_at is > 30 days ago (or null).
        Flags is_inspection_overdue = True and logs alert notifications.
        """
        threshold_days = settings.ALERTS_OVERDUE_DAYS # 30 days
        cutoff_date = datetime.utcnow() - timedelta(days=threshold_days)

        roads = db.query(RoadSegment).all()
        overdue_roads = []
        alerts_created = 0

        for r in roads:
            is_overdue = False
            days_ago = None
            if r.last_inspected_at is None:
                is_overdue = True
                days_ago = threshold_days + 1
            elif r.last_inspected_at < cutoff_date:
                is_overdue = True
                days_ago = (datetime.utcnow() - r.last_inspected_at).days

            r.is_inspection_overdue = is_overdue
            if is_overdue:
                overdue_roads.append({
                    "road_id": r.id,
                    "road_code": r.road_code,
                    "name": r.name,
                    "state": r.state,
                    "days_overdue": days_ago
                })

                # Log automated notification alert (SMS + Email)
                alert_msg = (
                    f"AUTOMATED ALERT: Inspection on road segment [{r.road_code}] - {r.name} "
                    f"is OVERDUE by {days_ago} days (> {threshold_days} days). Immediate field audit required."
                )

                log_entry = NotificationLog(
                    channel="SMS",
                    recipient="FERMA-Zonal-Engineer",
                    subject=f"OVERDUE ROAD INSPECTION: {r.road_code}",
                    message=alert_msg,
                    status="SENT"
                )
                db.add(log_entry)
                alerts_created += 1

        db.commit()
        return {
            "status": "success",
            "threshold_days": threshold_days,
            "total_overdue_roads": len(overdue_roads),
            "alerts_dispatched": alerts_created,
            "overdue_list": overdue_roads
        }

    @staticmethod
    def get_all_inspections(db: Session) -> List[Inspection]:
        return db.query(Inspection).order_by(Inspection.scheduled_date.desc()).all()
