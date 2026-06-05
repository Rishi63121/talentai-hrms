from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import Payroll
from backend.schemas.schemas import PayrollCreate

router = APIRouter()


@router.post("")
def create_payroll(
    payload: PayrollCreate,
    db: Session = Depends(get_db)
):

    net_salary = (
        payload.basic_salary
        + payload.bonus
        - payload.deductions
    )

    payroll = Payroll(
        employee_id=payload.employee_id,
        basic_salary=payload.basic_salary,
        bonus=payload.bonus,
        deductions=payload.deductions,
        net_salary=net_salary,
        month=payload.month
    )

    db.add(payroll)
    db.commit()
    db.refresh(payroll)

    return {
        "id": payroll.id,
        "employee_id": payroll.employee_id,
        "month": payroll.month,
        "basic_salary": payroll.basic_salary,
        "bonus": payroll.bonus,
        "deductions": payroll.deductions,
        "net_salary": payroll.net_salary
    }

@router.get("")
def get_payroll(db: Session = Depends(get_db)):
    return db.query(Payroll).all()