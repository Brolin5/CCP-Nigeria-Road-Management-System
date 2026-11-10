from fastapi import APIRouter
from app.routers.auth_router import router as auth_router
from app.routers.report_router import router as report_router
from app.routers.project_router import router as project_router
from app.routers.inspection_router import router as inspection_router
from app.routers.dashboard_router import router as dashboard_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(report_router)
api_router.include_router(project_router)
api_router.include_router(inspection_router)
api_router.include_router(dashboard_router)
