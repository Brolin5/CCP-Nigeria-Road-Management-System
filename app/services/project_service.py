from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model import RoadProject, ProjectMilestone, RoadSegment, User
from app.schemas.project_schema import (
    ProjectCreate,
    MilestoneCreate,
    MilestoneProgressUpdate,
    MilestoneReview
)

class ProjectService:
    @staticmethod
    def recalculate_project_progress(db: Session, project_id: int) -> float:
        """
        Recalculates the cumulative project progress percentage based on milestone weights:
        cumulative_progress = sum(percentage_weight * progress_pct_achieved / 100)
        """
        project = db.query(RoadProject).filter(RoadProject.id == project_id).first()
        if not project:
            return 0.0

        milestones = db.query(ProjectMilestone).filter(ProjectMilestone.project_id == project_id).all()
        if not milestones:
            return 0.0

        total_achieved = 0.0
        for m in milestones:
            total_achieved += (m.percentage_weight * (m.progress_pct_achieved / 100.0))

        # Clamp to 100.0 max
        project.current_progress_pct = round(min(total_achieved, 100.0), 2)
        if project.current_progress_pct >= 100.0:
            project.status = "Completed"
        elif project.current_progress_pct > 0.0 and project.status == "Not Started":
            project.status = "Ongoing"

        db.commit()
        db.refresh(project)
        return project.current_progress_pct

    @classmethod
    def create_project(cls, db: Session, project_in: ProjectCreate) -> RoadProject:
        # Validate road and contractor
        road = db.query(RoadSegment).filter(RoadSegment.id == project_in.road_id).first()
        if not road:
            raise HTTPException(status_code=404, detail="Assigned road segment not found.")

        contractor = db.query(User).filter(User.id == project_in.contractor_id).first()
        if not contractor:
            raise HTTPException(status_code=404, detail="Assigned contractor user not found.")

        # Check unique code
        if db.query(RoadProject).filter(RoadProject.project_code == project_in.project_code).first():
            raise HTTPException(status_code=400, detail="Project code already exists.")

        project = RoadProject(
            project_code=project_in.project_code,
            title=project_in.title,
            description=project_in.description,
            road_id=project_in.road_id,
            contractor_id=project_in.contractor_id,
            supervising_agency=project_in.supervising_agency,
            budget_naira=project_in.budget_naira,
            start_date=project_in.start_date,
            expected_completion_date=project_in.expected_completion_date
        )
        db.add(project)
        db.flush()

        if project_in.milestones:
            for m_in in project_in.milestones:
                m = ProjectMilestone(
                    project_id=project.id,
                    milestone_name=m_in.milestone_name,
                    milestone_order=m_in.milestone_order,
                    percentage_weight=m_in.percentage_weight,
                    progress_pct_achieved=0.0,
                    status="Pending"
                )
                db.add(m)

        db.commit()
        db.refresh(project)
        cls.recalculate_project_progress(db, project.id)
        return project

    @classmethod
    def submit_milestone_progress(
        cls, db: Session, milestone_id: int, update_in: MilestoneProgressUpdate
    ) -> ProjectMilestone:
        milestone = db.query(ProjectMilestone).filter(ProjectMilestone.id == milestone_id).first()
        if not milestone:
            raise HTTPException(status_code=404, detail=f"Milestone #{milestone_id} not found.")

        # Require photo evidence to ensure contractor transparency
        if not update_in.photo_evidence_url or not update_in.photo_evidence_url.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contractor on-site photo evidence URL is strictly mandatory before submitting progress."
            )

        milestone.progress_pct_achieved = update_in.progress_pct_achieved
        milestone.photo_evidence_url = update_in.photo_evidence_url
        milestone.contractor_notes = update_in.contractor_notes
        milestone.status = "Pending Inspection"
        milestone.submitted_at = datetime.utcnow()

        db.commit()
        cls.recalculate_project_progress(db, milestone.project_id)
        db.refresh(milestone)
        return milestone

    @classmethod
    def review_milestone(
        cls, db: Session, milestone_id: int, review_in: MilestoneReview
    ) -> ProjectMilestone:
        milestone = db.query(ProjectMilestone).filter(ProjectMilestone.id == milestone_id).first()
        if not milestone:
            raise HTTPException(status_code=404, detail=f"Milestone #{milestone_id} not found.")

        milestone.status = review_in.status
        milestone.inspected_at = datetime.utcnow()
        db.commit()
        cls.recalculate_project_progress(db, milestone.project_id)
        db.refresh(milestone)
        return milestone

    @staticmethod
    def get_all_projects(db: Session, skip: int = 0, limit: int = 50) -> List[RoadProject]:
        return db.query(RoadProject).order_by(RoadProject.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_project_by_id(db: Session, project_id: int) -> RoadProject:
        project = db.query(RoadProject).filter(RoadProject.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project #{project_id} not found.")
        return project
