from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import Attendance
from backend.schemas.schemas import AttendanceCreate

router = APIRouter()


@router.post("")
def mark_attendance(payload: AttendanceCreate,
                    db: Session = Depends(get_db)):

    record = Attendance(
        employee_id=payload.employee_id,
        status=payload.status
    )

    db.add(record)
    db.commit()

    return {"message": "Attendance marked"}


@router.get("")
def get_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()