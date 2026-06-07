from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import recruiters
from backend.routers import (
    auth,
    jobs,
    resumes,
    candidates,
    interview,
    onboarding,
    dashboard,
    employees,
    attendance,
    payroll,
    performance
)

from database.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TalentAI HRMS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# AUTH
# =========================

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

# =========================
# RECRUITMENT
# =========================

app.include_router(
    jobs.router,
    prefix="/jobs",
    tags=["Jobs"]
)

app.include_router(
    resumes.router,
    prefix="/resumes",
    tags=["Resumes"]
)

app.include_router(
    candidates.router,
    prefix="/candidates",
    tags=["Candidates"]
)

app.include_router(
    interview.router,
    prefix="/interview",
    tags=["Interview"]
)

# =========================
# HRMS
# =========================

app.include_router(
    employees.router,
    prefix="/employees",
    tags=["Employees"]
)

app.include_router(
    attendance.router,
    prefix="/attendance",
    tags=["Attendance"]
)

app.include_router(
    payroll.router,
    prefix="/payroll",
    tags=["Payroll"]
)

app.include_router(
    performance.router,
    prefix="/performance",
    tags=["Performance"]
)

# =========================
# OTHER MODULES
# =========================

app.include_router(
    onboarding.router,
    prefix="/onboarding",
    tags=["Onboarding"]
)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "TalentAI HRMS API is running"
    }

app.include_router(
    recruiters.router,
    prefix="/recruiters",
    tags=["Recruiters"]
)