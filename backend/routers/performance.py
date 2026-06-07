from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from backend.models.models import PerformanceReview, Employee
from backend.schemas.schemas import PerformanceCreate
from backend.services.auth_service import get_current_user

router = APIRouter()


@router.post("")
def add_review(
    payload: PerformanceCreate,
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == payload.employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    review = PerformanceReview(
        employee_id=payload.employee_id,
        rating=payload.rating,
        comments=payload.comments
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "id": review.id,
        "employee_id": review.employee_id,
        "employee_name": employee.name,
        "rating": review.rating,
        "comments": review.comments,
        "created_at": review.created_at
    }


@router.put("/{review_id}")
def update_review(
    review_id: int,
    payload: PerformanceCreate,
    db: Session = Depends(get_db)
):

    review = db.query(PerformanceReview).filter(
        PerformanceReview.id == review_id
    ).first()

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    review.employee_id = payload.employee_id
    review.rating = payload.rating
    review.comments = payload.comments

    db.commit()
    db.refresh(review)

    return {
        "message": "Review updated successfully"
    }


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db)
):

    review = db.query(PerformanceReview).filter(
        PerformanceReview.id == review_id
    ).first()

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    db.delete(review)
    db.commit()

    return {
        "message": "Review deleted successfully"
    }


@router.get("")
def get_reviews(
    db: Session = Depends(get_db)
):

    reviews = (
        db.query(PerformanceReview)
        .order_by(PerformanceReview.created_at.desc())
        .all()
    )

    result = []

    for review in reviews:

        employee = db.query(Employee).filter(
            Employee.id == review.employee_id
        ).first()

        result.append({
            "id": review.id,
            "employee_id": review.employee_id,
            "employee_name": employee.name if employee else "Unknown",
            "rating": review.rating,
            "comments": review.comments,
            "created_at": review.created_at
        })

    return result


@router.get("/my")
def get_my_reviews(
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

    reviews = (
        db.query(PerformanceReview)
        .filter(
            PerformanceReview.employee_id == employee.id
        )
        .order_by(
            PerformanceReview.created_at.desc()
        )
        .all()
    )

    result = []

    for review in reviews:
        result.append({
            "id": review.id,
            "employee_id": review.employee_id,
            "employee_name": employee.name,
            "rating": review.rating,
            "comments": review.comments,
            "created_at": review.created_at
        })

    return result