from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import PerformanceReview
from backend.schemas.schemas import PerformanceCreate

router = APIRouter()


@router.post("")
def add_review(payload: PerformanceCreate,
               db: Session = Depends(get_db)):

    review = PerformanceReview(**payload.dict())

    db.add(review)
    db.commit()

    return review


@router.get("")
def get_reviews(db: Session = Depends(get_db)):
    return db.query(PerformanceReview).all()