from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import Attendance, Employee
from backend.schemas.schemas import AttendanceCreate
from backend.services.auth_service import get_current_user

router = APIRouter()


@router.post("")
def mark_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == payload.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    record = Attendance(
        employee_id=payload.employee_id,
        status=payload.status
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "Attendance marked successfully"
    }


@router.get("")
def get_attendance(
    db: Session = Depends(get_db)
):
    records = db.query(Attendance).all()

    result = []

    for record in records:
        employee = db.query(Employee).filter(
            Employee.id == record.employee_id
        ).first()

        result.append({
            "id": record.id,
            "employee_id": record.employee_id,
            "employee_name": employee.name if employee else "Unknown",
            "date": record.date,
            "status": record.status
        })

    return result


@router.get("/my")
def get_my_attendance(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(Employee.email == current_user["sub"])
        .first()
    )

    if not employee:
        return []

    records = (
        db.query(Attendance)
        .filter(Attendance.employee_id == employee.id)
        .all()
    )

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "employee_id": record.employee_id,
            "employee_name": employee.name,
            "date": record.date,
            "status": record.status
        })

    return result