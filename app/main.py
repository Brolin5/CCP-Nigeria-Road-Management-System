import sys
import os

# Fix Windows console UTF-8 encoding for Unicode/emojis
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Ensure project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import settings
from app.database import get_db, engine
from app.route import api_router
from app.model import (
    Base,
    Role,
    User,
    user_roles,
    RoadSegment,
    RoadReport,
    RoadProject,
    ProjectMilestone,
    Inspection,
    NotificationLog,
    AuditLog
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nrms")

print(f"🔗 [NRMS] Connecting to Database: {settings.DATABASE_URL}")

def run_migrations() -> None:
    """
    Programmatic Alembic migration routine executed at application startup.
    Ensures zero-touch migration to HEAD before serving incoming HTTP traffic.
    """
    project_root = Path(__file__).resolve().parent.parent
    alembic_ini_path = project_root / "alembic.ini"
    alembic_dir = project_root / "alembic"

    print(f"🔍 [NRMS] Checking Alembic configuration at: {alembic_ini_path}")
    if not alembic_ini_path.exists():
        raise FileNotFoundError(f"Alembic config not found at {alembic_ini_path}")

    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.config_ini_section = "alembic"
    alembic_cfg.set_main_option("script_location", str(alembic_dir))

    print("⚙️ [NRMS] Applying database migrations to HEAD...")
    command.upgrade(alembic_cfg, "head")
    print("✅ [NRMS] Database schema is up to date.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan Context Manager: runs migrations on startup.
    """
    print("🌟 [NRMS] Nigeria Road Management System API starting up...")
    try:
        await asyncio.to_thread(run_migrations)
    except Exception as e:
        print(f"❌ [NRMS] Startup migration check: {e}")
    yield
    print("🛑 [NRMS] Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Citizen-Centric Platform for Road Monitoring, Crowdsourced Reporting, Contractor Tracking, and Automated Inspection Alerts.",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all business routes under /api/v1
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/doc", include_in_schema=False)
def redirect_to_docs():
    """Redirect /doc directly to interactive /docs Swagger UI"""
    return RedirectResponse(url="/docs")

@app.get("/", tags=["System"])
def read_root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "online",
        "api_docs": "/docs",
        "api_endpoints": {
            "auth": f"{settings.API_V1_PREFIX}/auth",
            "reports": f"{settings.API_V1_PREFIX}/reports",
            "projects": f"{settings.API_V1_PREFIX}/projects",
            "inspections": f"{settings.API_V1_PREFIX}/inspections",
            "dashboard": f"{settings.API_V1_PREFIX}/dashboard"
        }
    }

@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected (MySQL 8.0)"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database unreachable: {e}"
        )

@app.post("/seed-nrms-data", tags=["Seed & Demo"])
def seed_nrms_data(db: Session = Depends(get_db)):
    """
    Seeds initial system roles, sample roads, contractor projects, and sample defect reports.
    """
    roles_data = [
        ("citizen", "Commuters and road users reporting defects and violations"),
        ("contractor", "Licensed road construction and maintenance contractors"),
        ("inspector", "Field engineers and quality assurance officers"),
        ("admin", "Road authorities (FERMA / Ministry of Works officials)")
    ]
    role_map = {}
    for r_name, r_desc in roles_data:
        existing = db.query(Role).filter(Role.name == r_name).first()
        if not existing:
            new_role = Role(name=r_name, description=r_desc)
            db.add(new_role)
            db.flush()
            role_map[r_name] = new_role
        else:
            role_map[r_name] = existing

    admin_user = db.query(User).filter(User.username == "ferma_admin").first()
    if not admin_user:
        admin_user = User(
            username="ferma_admin",
            email="admin@ferma.gov.ng",
            hashed_password="pbkdf2:sha256:100000$mock_salt$mock_hash",
            full_name="Engr. Babatunde Lawal",
            phone_number="+2348030000001",
            organization="FERMA Headquarters Abuja"
        )
        admin_user.roles.append(role_map["admin"])
        db.add(admin_user)

    contractor_user = db.query(User).filter(User.username == "jb_contractor").first()
    if not contractor_user:
        contractor_user = User(
            username="jb_contractor",
            email="projects@juliusberger-demo.ng",
            hashed_password="pbkdf2:sha256:100000$mock_salt$mock_hash",
            full_name="Julius Berger Civil Engineering",
            phone_number="+2348020000002",
            organization="Julius Berger Nigeria Plc"
        )
        contractor_user.roles.append(role_map["contractor"])
        db.add(contractor_user)

    citizen_user = db.query(User).filter(User.username == "commuter_john").first()
    if not citizen_user:
        citizen_user = User(
            username="commuter_john",
            email="citizen.john@example.com",
            hashed_password="pbkdf2:sha256:100000$mock_salt$mock_hash",
            full_name="John Chinedu",
            phone_number="+2348140000003",
            organization="Private Citizen"
        )
        citizen_user.roles.append(role_map["citizen"])
        db.add(citizen_user)

    db.flush()

    sample_road = db.query(RoadSegment).filter(RoadSegment.road_code == "FED-A234-ABJ").first()
    if not sample_road:
        sample_road = RoadSegment(
            road_code="FED-A234-ABJ",
            name="Abuja-Keffi Dual Carriageway",
            classification="Federal",
            state="FCT",
            lga="Abuja Municipal / Karu",
            length_km=43.5,
            start_latitude=9.0435,
            start_longitude=7.4988,
            end_latitude=8.8471,
            end_longitude=7.8732,
            condition_status="Poor",
            is_inspection_overdue=True
        )
        db.add(sample_road)
        db.flush()

    sample_report = db.query(RoadReport).filter(RoadReport.ticket_number == "NRMS-2026-AB001").first()
    if not sample_report:
        sample_report = RoadReport(
            ticket_number="NRMS-2026-AB001",
            report_type="defect",
            category="Deep Pothole / Crater",
            description="Severe cluster of deep potholes causing sharp vehicular swerving near Kugbo hill bridge.",
            latitude=9.0142,
            longitude=7.5518,
            location_description="Opposite Kugbo mechanic village, Karu axis",
            photo_url="https://res.cloudinary.com/nrms/image/upload/v1/samples/pothole_kugbo.jpg",
            severity="Critical",
            status="Under Review",
            citizen_id=citizen_user.id,
            road_id=sample_road.id
        )
        db.add(sample_report)

    sample_project = db.query(RoadProject).filter(RoadProject.project_code == "PRJ-2026-FCT-001").first()
    if not sample_project:
        sample_project = RoadProject(
            project_code="PRJ-2026-FCT-001",
            title="Kugbo to Karu Critical Pavement Overlay & Drainage Rehabilitation",
            description="Emergency bituminous overlay and concrete side drain installation.",
            road_id=sample_road.id,
            contractor_id=contractor_user.id,
            supervising_agency="Federal Ministry of Works / FERMA",
            budget_naira=450000000.00,
            current_progress_pct=35.0,
            status="Ongoing"
        )
        db.add(sample_project)
        db.flush()

        m1 = ProjectMilestone(
            project_id=sample_project.id,
            milestone_name="Stage 1: Sub-base Scarification & Base Proof Rolling",
            milestone_order=1,
            percentage_weight=35.0,
            progress_pct_achieved=35.0,
            photo_evidence_url="https://res.cloudinary.com/nrms/image/upload/v1/samples/scarification_stage1.jpg",
            contractor_notes="Completed 4.2km scarification. Density test certificates ready.",
            status="Approved"
        )
        m2 = ProjectMilestone(
            project_id=sample_project.id,
            milestone_name="Stage 2: 60mm Bituminous Asphalt Binder Course",
            milestone_order=2,
            percentage_weight=40.0,
            progress_pct_achieved=0.0,
            status="Pending"
        )
        db.add_all([m1, m2])

    db.commit()
    return {
        "status": "success",
        "message": "NRMS initial seed data provisioned successfully!"
    }

if __name__ == "__main__":
    print("🌐 [NRMS] Starting Uvicorn server on http://127.0.0.1:8000 ...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
