from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.dashboard_schema import DashboardKPIResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Officials GIS Dashboard & Analytics"])

@router.get("/kpis", response_model=DashboardKPIResponse)
def get_dashboard_kpis(db: Session = Depends(get_db)):
    """
    Returns executive summary indicators: total roads, critical roads, total reports,
    pending citizen reports, active contractor projects, and overdue inspections.
    """
    return DashboardService.get_kpis(db)

@router.get("/map-geojson", response_model=Dict[str, Any])
def get_map_geojson(db: Session = Depends(get_db)):
    """
    Returns GeoJSON FeatureCollection containing all geolocated defect/violation reports
    and road infrastructure assets for direct consumption by Leaflet.js / OpenStreetMap.
    """
    return DashboardService.get_map_geojson(db)
