import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import Job, CandidateScore
from backend.schemas.schemas import JobRequest, JobResponse
from backend.services.auth_service import get_current_user

router = APIRouter()


# ==========================================
# CREATE JOB
# ==========================================

@router.post("", response_model=JobResponse)
def create_job(
    payload: JobRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    job = Job(
        title=payload.title,
        description=payload.description,
        required_skills=json.dumps(payload.required_skills),
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return JobResponse(
        job_id=job.id,
        message="Job Created"
    )


# ==========================================
# LIST JOBS
# ==========================================

@router.get("")
def list_jobs(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()

    result = []

    for job in jobs:

        applicant_count = (
            db.query(CandidateScore)
            .filter(CandidateScore.job_id == job.id)
            .count()
        )

        result.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "required_skills": json.loads(
                job.required_skills or "[]"
            ),
            "created_at": job.created_at,
            "applicant_count": applicant_count,
        })

    return result


# ==========================================
# GET SINGLE JOB
# ==========================================

@router.get("/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    applicant_count = (
        db.query(CandidateScore)
        .filter(CandidateScore.job_id == job.id)
        .count()
    )

    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "required_skills": json.loads(
            job.required_skills or "[]"
        ),
        "created_at": job.created_at,
        "applicant_count": applicant_count,
    }


# ==========================================
# DELETE JOB
# ==========================================

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted"
    }