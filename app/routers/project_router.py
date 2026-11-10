from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.project_schema import (
    ProjectCreate,
    ProjectResponse,
    MilestoneProgressUpdate,
    MilestoneReview,
    MilestoneResponse
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Contractor Tracking & Milestones (Data Flow F2)"])

@router.get("/", response_model=List[ProjectResponse])
def list_projects(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    List all ongoing, under-review, and completed road construction projects.
    """
    return ProjectService.get_all_projects(db, skip=skip, limit=limit)

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db)):
    """
    Award and register a new road construction or rehabilitation contract with milestones.
    """
    return ProjectService.create_project(db, project_in)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_details(project_id: int, db: Session = Depends(get_db)):
    """
    Retrieve project details along with its milestone completion status.
    """
    return ProjectService.get_project_by_id(db, project_id)

@router.post(
    "/{project_id}/milestones/{milestone_id}/progress",
    response_model=MilestoneResponse
)
def upload_milestone_progress(
    project_id: int,
    milestone_id: int,
    progress_in: MilestoneProgressUpdate,
    db: Session = Depends(get_db)
):
    """
    Data Flow F2: Contractor Progress Upload.
    Contractor submits stage completion with mandatory on-site photo evidence.
    Automatically recalculates total project progress percentage.
    """
    return ProjectService.submit_milestone_progress(db, milestone_id, progress_in)

@router.post(
    "/{project_id}/milestones/{milestone_id}/review",
    response_model=MilestoneResponse
)
def review_milestone(
    project_id: int,
    milestone_id: int,
    review_in: MilestoneReview,
    db: Session = Depends(get_db)
):
    """
    Supervising Official / Field Inspector approves or rejects submitted milestone evidence.
    """
    return ProjectService.review_milestone(db, milestone_id, review_in)
