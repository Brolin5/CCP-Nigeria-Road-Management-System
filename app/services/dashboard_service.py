from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.model import RoadSegment, RoadReport, RoadProject, Inspection
from app.schemas.dashboard_schema import DashboardKPIResponse

class DashboardService:
    @staticmethod
    def get_kpis(db: Session) -> DashboardKPIResponse:
        total_roads = db.query(RoadSegment).count()
        critical_roads = db.query(RoadSegment).filter(RoadSegment.condition_status == "Critical").count()
        total_reports = db.query(RoadReport).count()
        pending_reports = db.query(RoadReport).filter(RoadReport.status.in_(["Pending", "Under Review"])).count()
        ongoing_projects = db.query(RoadProject).filter(RoadProject.status == "Ongoing").count()
        overdue_inspections = db.query(RoadSegment).filter(RoadSegment.is_inspection_overdue == True).count()

        return DashboardKPIResponse(
            total_roads=total_roads,
            critical_roads=critical_roads,
            total_reports=total_reports,
            pending_reports=pending_reports,
            ongoing_projects=ongoing_projects,
            overdue_inspections=overdue_inspections
        )

    @staticmethod
    def get_map_geojson(db: Session) -> Dict[str, Any]:
        """
        Formats all crowdsourced reports and road coordinates into standard GeoJSON 
        for zero-friction rendering in Leaflet.js + OpenStreetMap.
        """
        features: List[Dict[str, Any]] = []

        # 1. Reports features
        reports = db.query(RoadReport).all()
        for r in reports:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [r.longitude, r.latitude]
                },
                "properties": {
                    "id": r.id,
                    "ticket_number": r.ticket_number,
                    "type": "report",
                    "report_type": r.report_type,
                    "category": r.category,
                    "severity": r.severity,
                    "status": r.status,
                    "photo_url": r.photo_url,
                    "description": r.description,
                    "is_duplicate": r.is_duplicate,
                    "created_at": r.created_at.isoformat() if r.created_at else None
                }
            })

        # 2. Roads features
        roads = db.query(RoadSegment).all()
        for road in roads:
            if road.start_longitude and road.start_latitude:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [road.start_longitude, road.start_latitude]
                    },
                    "properties": {
                        "id": road.id,
                        "type": "road_asset",
                        "road_code": road.road_code,
                        "name": road.name,
                        "state": road.state,
                        "classification": road.classification,
                        "condition": road.condition_status,
                        "is_overdue": road.is_inspection_overdue
                    }
                })

        return {
            "type": "FeatureCollection",
            "features": features
        }
