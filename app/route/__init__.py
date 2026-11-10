from fastapi import APIRouter
from .user_route import router as user_router
from .role_route import router as role_router
from .road_route import router as road_router
from .report_route import router as report_router
from .project_route import router as project_router
from .milestone_route import router as milestone_router
from .inspection_route import router as inspection_router
from .notification_route import router as notification_router
from .audit_log_route import router as audit_log_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.auth_router import router as auth_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(role_router)
api_router.include_router(road_router)
api_router.include_router(report_router)
api_router.include_router(project_router)
api_router.include_router(milestone_router)
api_router.include_router(inspection_router)
api_router.include_router(notification_router)
api_router.include_router(audit_log_router)
api_router.include_router(dashboard_router)
api_router.include_router(auth_router)

__all__ = [
    "api_router",
    "user_router",
    "role_router",
    "road_router",
    "report_router",
    "project_router",
    "milestone_router",
    "inspection_router",
    "notification_router",
    "audit_log_router",
    "dashboard_router",
    "auth_router",
]
