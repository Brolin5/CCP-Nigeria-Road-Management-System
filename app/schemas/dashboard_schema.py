from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DashboardKPIResponse(BaseModel):
    total_roads: int
    critical_roads: int
    total_reports: int
    pending_reports: int
    ongoing_projects: int
    overdue_inspections: int

class MapFeatureGeometry(BaseModel):
    type: str = "Point"
    coordinates: List[float] # [longitude, latitude]

class MapFeature(BaseModel):
    type: str = "Feature"
    geometry: MapFeatureGeometry
    properties: Dict[str, Any]

class GeoJSONResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[MapFeature]
