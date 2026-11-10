from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.schemas.report_schema import ReportCreate, ReportResponse, ReportStatusUpdate, ReportListResponse
from app.schemas.project_schema import ProjectCreate, ProjectResponse, MilestoneCreate, MilestoneProgressUpdate, MilestoneResponse
from app.schemas.inspection_schema import InspectionCreate, InspectionResponse, InspectionComplete, OverdueRoadResponse
from app.schemas.dashboard_schema import DashboardKPIResponse, GeoJSONResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
    "ReportCreate",
    "ReportResponse",
    "ReportStatusUpdate",
    "ReportListResponse",
    "ProjectCreate",
    "ProjectResponse",
    "MilestoneCreate",
    "MilestoneProgressUpdate",
    "MilestoneResponse",
    "InspectionCreate",
    "InspectionResponse",
    "InspectionComplete",
    "OverdueRoadResponse",
    "DashboardKPIResponse",
    "GeoJSONResponse"
]
