from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from backend.models.models import Candidate, Job, CandidateScore
from backend.schemas.schemas import DashboardResponse
from backend.services.auth_service import get_current_user

router = APIRouter()


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    total_candidates = db.query(Candidate).count()
    total_jobs = db.query(Job).count()
    screened = db.query(CandidateScore.candidate_id).distinct().count()
    return DashboardResponse(
        total_candidates=total_candidates,
        jobs=total_jobs,
        screened=screened,
    )
