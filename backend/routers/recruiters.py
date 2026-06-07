from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import User

router = APIRouter()


@router.get("")
def get_recruiters(
    db: Session = Depends(get_db)
):

    recruiters = (
        db.query(User)
        .filter(User.role == "recruiter")
        .all()
    )

    result = []

    for recruiter in recruiters:

        result.append({
            "id": recruiter.id,
            "name": recruiter.name,
            "email": recruiter.email,
            "region": "India",
            "hire_count": 0
        })

    return result