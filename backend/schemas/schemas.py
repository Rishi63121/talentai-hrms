from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    role: str


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "recruiter"


# ── Jobs ──────────────────────────────────────────────────────────────────────

class JobRequest(BaseModel):
    title: str
    description: str
    required_skills: List[str]


class JobResponse(BaseModel):
    job_id: int
    message: str


class JobListItem(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


# ── Resumes ───────────────────────────────────────────────────────────────────

class ResumeUploadResponse(BaseModel):
    candidate_id: int
    message: str


# ── Candidates ────────────────────────────────────────────────────────────────

class ScreenRequest(BaseModel):
    candidate_id: int
    job_id: int


class CandidateScoreResponse(BaseModel):
    candidate_id: int
    score: float
    matched_skills: List[str]
    missing_skills: List[str]


class CandidateRankItem(BaseModel):
    candidate_id: int
    rank: int
    score: float


class CandidateDetail(BaseModel):
    candidate_id: int
    name: str
    score: Optional[float] = None
    email: Optional[str] = None
    education: Optional[str] = None
    experience_years: Optional[int] = None


# ── Interview ─────────────────────────────────────────────────────────────────

class InterviewQuestionRequest(BaseModel):
    candidate_id: int


class InterviewQuestionResponse(BaseModel):
    questions: List[str]


# ── Onboarding ────────────────────────────────────────────────────────────────

class OnboardingRequest(BaseModel):
    candidate_id: int


class OnboardingResponse(BaseModel):
    status: str


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    total_candidates: int
    jobs: int
    screened: int
# ================= EMPLOYEE =================

class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str
    designation: str
    salary: float


class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True


# ================= ATTENDANCE =================

class AttendanceCreate(BaseModel):
    employee_id: int
    status: str


# ================= PAYROLL =================

class PayrollCreate(BaseModel):
    employee_id: int
    basic_salary: float
    bonus: float = 0
    deductions: float = 0
    month: str


# ================= PERFORMANCE =================

class PerformanceCreate(BaseModel):
    employee_id: int
    rating: int
    comments: str