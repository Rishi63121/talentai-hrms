import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import (
    Candidate,
    Job,
    CandidateScore,
    OnboardingRecord,
)
from backend.schemas.schemas import (
    ScreenRequest,
    CandidateScoreResponse,
    CandidateRankItem,
)
from backend.services.auth_service import get_current_user
from backend.services.ai_service import score_candidate
from backend.services.resume_service import parse_resume
from backend.services.ranking_service import recompute_ranks

router = APIRouter()


# =====================================================
# SCREEN CANDIDATE
# =====================================================

@router.post("/screen", response_model=CandidateScoreResponse)
def screen_candidate(
    payload: ScreenRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == payload.candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    job = (
        db.query(Job)
        .filter(Job.id == payload.job_id)
        .first()
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    required_skills = json.loads(job.required_skills or "[]")

    resume_text = ""
    candidate_skills = []

    if candidate.resume_path:
        parsed = parse_resume(candidate.resume_path)

        resume_text = parsed.get("raw_text", "")
        candidate_skills = parsed.get("skills", [])

    result = score_candidate(
        resume_text=resume_text,
        candidate_skills=candidate_skills,
        job_title=job.title,
        job_description=job.description or "",
        required_skills=required_skills,
    )

    score_record = (
        db.query(CandidateScore)
        .filter(
            CandidateScore.candidate_id == payload.candidate_id,
            CandidateScore.job_id == payload.job_id,
        )
        .first()
    )

    if score_record:
        score_record.match_score = result["match_score"]
        score_record.matched_skills = json.dumps(result["matched_skills"])
        score_record.missing_skills = json.dumps(result["missing_skills"])

    else:
        score_record = CandidateScore(
            candidate_id=payload.candidate_id,
            job_id=payload.job_id,
            match_score=result["match_score"],
            matched_skills=json.dumps(result["matched_skills"]),
            missing_skills=json.dumps(result["missing_skills"]),
        )

        db.add(score_record)

    db.commit()

    recompute_ranks(payload.job_id, db)

    return CandidateScoreResponse(
        candidate_id=payload.candidate_id,
        score=result["match_score"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
    )


# =====================================================
# RANKINGS
# =====================================================

@router.get("/rankings", response_model=List[CandidateRankItem])
def get_rankings(
    job_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    query = db.query(CandidateScore)

    if job_id:
        query = query.filter(CandidateScore.job_id == job_id)

    scores = query.order_by(CandidateScore.rank.asc()).all()

    return [
        CandidateRankItem(
            candidate_id=s.candidate_id,
            rank=s.rank,
            score=s.match_score,
        )
        for s in scores
    ]


# =====================================================
# SINGLE CANDIDATE DETAILS
# =====================================================

@router.get("/{candidate_id}")
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found",
        )

    latest_score = (
        db.query(CandidateScore)
        .filter(CandidateScore.candidate_id == candidate_id)
        .order_by(CandidateScore.match_score.desc())
        .first()
    )

    onboarding = (
        db.query(OnboardingRecord)
        .filter(OnboardingRecord.candidate_id == candidate_id)
        .first()
    )

    score = None
    rank = None
    matched_skills = []
    missing_skills = []
    job_title = None

    if latest_score:
        score = latest_score.match_score
        rank = latest_score.rank

        matched_skills = json.loads(
            latest_score.matched_skills or "[]"
        )

        missing_skills = json.loads(
            latest_score.missing_skills or "[]"
        )

        job = (
            db.query(Job)
            .filter(Job.id == latest_score.job_id)
            .first()
        )

        if job:
            job_title = job.title

    return {
        "candidate_id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "education": candidate.education,
        "experience_years": candidate.experience_years,

        "score": score,
        "rank": rank,

        "matched_skills": matched_skills,
        "missing_skills": missing_skills,

        "job_title": job_title,

        "status": (
            onboarding.status
            if onboarding
            else "not_started"
        ),

        "resume_path": candidate.resume_path,
        "created_at": candidate.created_at,
    }


# =====================================================
# ALL CANDIDATES
# =====================================================

@router.get("")
def list_candidates(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    candidates = (
        db.query(Candidate)
        .order_by(Candidate.created_at.desc())
        .all()
    )

    result = []

    for candidate in candidates:

        latest_score = (
            db.query(CandidateScore)
            .filter(
                CandidateScore.candidate_id == candidate.id
            )
            .order_by(
                CandidateScore.match_score.desc()
            )
            .first()
        )

        onboarding = (
            db.query(OnboardingRecord)
            .filter(
                OnboardingRecord.candidate_id == candidate.id
            )
            .first()
        )

        job_title = None
        matched_skills = []
        missing_skills = []

        if latest_score:

            matched_skills = json.loads(
                latest_score.matched_skills or "[]"
            )

            missing_skills = json.loads(
                latest_score.missing_skills or "[]"
            )

            job = (
                db.query(Job)
                .filter(Job.id == latest_score.job_id)
                .first()
            )

            if job:
                job_title = job.title

        result.append({
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "experience_years": candidate.experience_years,

            "score": (
                latest_score.match_score
                if latest_score
                else None
            ),

            "rank": (
                latest_score.rank
                if latest_score
                else None
            ),

            "matched_skills": matched_skills,
            "missing_skills": missing_skills,

            "job_title": job_title,

            "status": (
                onboarding.status
                if onboarding
                else "not_started"
            ),

            "created_at": candidate.created_at,
        })

    return result