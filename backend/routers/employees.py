from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import Employee, User
from backend.schemas.schemas import EmployeeCreate
from backend.services.auth_service import hash_password

router = APIRouter()


@router.post("")
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db)
):
    # Create employee record
    employee = Employee(**payload.dict())

    db.add(employee)
    db.commit()
    db.refresh(employee)

    # Create login account if it doesn't already exist
    existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if not existing_user:
        user = User(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password("Temp@123"),
            role="employee"
        )

        db.add(user)
        db.commit()

    return {
        "message": "Employee created successfully",
        "default_password": "Temp@123",
        "employee": employee
    }


@router.get("")
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()