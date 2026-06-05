import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from backend.models.models import Job
from backend.schemas.schemas import JobRequest, JobResponse, JobListItem
from backend.services.auth_service import get_current_user
from typing import List

router = APIRouter()


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
    return JobResponse(job_id=job.id, message="Job Created")


@router.get("", response_model=List[JobListItem])
def list_jobs(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return [JobListItem(id=j.id, title=j.title) for j in jobs]


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "required_skills": json.loads(job.required_skills or "[]"),
        "created_at": job.created_at,
    }


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}
