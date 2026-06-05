from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from backend.models.models import Candidate, OnboardingRecord
from backend.schemas.schemas import OnboardingRequest, OnboardingResponse
from backend.services.auth_service import get_current_user

router = APIRouter()

VALID_STATUSES = {"pending", "in_progress", "completed", "rejected"}


@router.post("/create", response_model=OnboardingResponse)
def create_onboarding(
    payload: OnboardingRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    candidate = db.query(Candidate).filter(Candidate.id == payload.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    existing = (
        db.query(OnboardingRecord)
        .filter(OnboardingRecord.candidate_id == payload.candidate_id)
        .first()
    )
    if existing:
        return OnboardingResponse(status=existing.status)

    record = OnboardingRecord(candidate_id=payload.candidate_id, status="created")
    db.add(record)
    db.commit()
    return OnboardingResponse(status="created")


@router.patch("/{candidate_id}/status")
def update_status(
    candidate_id: int,
    status: str,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    if status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Status must be one of {VALID_STATUSES}")
    record = (
        db.query(OnboardingRecord)
        .filter(OnboardingRecord.candidate_id == candidate_id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Onboarding record not found")
    record.status = status
    db.commit()
    return {"candidate_id": candidate_id, "status": status}


@router.get("")
def list_onboarding(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    records = db.query(OnboardingRecord).all()
    return [
        {"candidate_id": r.candidate_id, "status": r.status, "created_at": r.created_at}
        for r in records
    ]
