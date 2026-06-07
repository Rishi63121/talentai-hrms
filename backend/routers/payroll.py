from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import Payroll, Employee
from backend.schemas.schemas import PayrollCreate
from backend.services.auth_service import get_current_user

router = APIRouter()


@router.post("")
def create_payroll(
    payload: PayrollCreate,
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
        "employee_name": employee.name,
        "month": payroll.month,
        "basic_salary": payroll.basic_salary,
        "bonus": payroll.bonus,
        "deductions": payroll.deductions,
        "net_salary": payroll.net_salary
    }


@router.get("")
def get_payroll(
    db: Session = Depends(get_db)
):

    records = db.query(Payroll).all()

    result = []

    for record in records:

        employee = db.query(Employee).filter(
            Employee.id == record.employee_id
        ).first()

        result.append({
            "id": record.id,
            "employee_id": record.employee_id,
            "employee_name": employee.name if employee else "Unknown",
            "month": record.month,
            "basic_salary": record.basic_salary,
            "bonus": record.bonus,
            "deductions": record.deductions,
            "net_salary": record.net_salary
        })

    return result


@router.get("/my")
def get_my_payroll(
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
        db.query(Payroll)
        .filter(Payroll.employee_id == employee.id)
        .all()
    )

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "employee_id": record.employee_id,
            "employee_name": employee.name,
            "month": record.month,
            "basic_salary": record.basic_salary,
            "bonus": record.bonus,
            "deductions": record.deductions,
            "net_salary": record.net_salary
        })

    return result