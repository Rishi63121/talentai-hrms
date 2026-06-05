from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import Employee
from backend.schemas.schemas import EmployeeCreate

router = APIRouter()


@router.post("")
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(**payload.dict())

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


@router.get("")
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()