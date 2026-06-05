import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from backend.models.models import Candidate
from backend.schemas.schemas import ResumeUploadResponse
from backend.services.auth_service import get_current_user
from backend.services.resume_service import parse_resume

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # Save file to disk
    safe_name = file.filename.replace(" ", "_")
    dest_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse resume
    parsed = parse_resume(dest_path)

    # Upsert candidate (by email if available)
    email = parsed.get("email") or f"unknown_{safe_name}@talentai.local"
    candidate = db.query(Candidate).filter(Candidate.email == email).first()

    if candidate:
        candidate.name = parsed["name"] or candidate.name
        candidate.education = parsed["education"] or candidate.education
        candidate.experience_years = parsed["experience_years"] or candidate.experience_years
        candidate.resume_path = dest_path
    else:
        candidate = Candidate(
            name=parsed["name"] or "Unknown",
            email=email,
            education=parsed["education"],
            experience_years=parsed["experience_years"],
            resume_path=dest_path,
        )
        db.add(candidate)

    db.commit()
    db.refresh(candidate)
    return ResumeUploadResponse(candidate_id=candidate.id, message="Resume Uploaded")
