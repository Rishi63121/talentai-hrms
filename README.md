# TalentAI HRMS — Backend

## Quick Start

```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Copy and configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
GROQ_API_KEY=your_groq_api_key
 SECRET_KEY=your_secret_key 
 ALGORITHM=HS256 
 ACCESS_TOKEN_EXPIRE_MINUTES=30
# 3. Seed the database (creates admin user)
python seed.py

# 4. Start the API server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs available at: http://localhost:8000/docs

## Default Credentials
- Email: `admin@talentai.com`
- Password: `admin123`

## Folder Structure
```
talentai-hrms/
├── backend/
│   ├── main.py               # FastAPI app + router registration
│   ├── routers/
│   │   ├── auth.py           # POST /auth/login, /auth/register
│   │   ├── jobs.py           # CRUD /jobs
│   │   ├── resumes.py        # POST /resumes/upload
│   │   ├── candidates.py     # /candidates/screen, /rankings, /{id}
│   │   ├── interview.py      # POST /interview/questions
│   │   ├── onboarding.py     # POST /onboarding/create
│   │   └── dashboard.py      # GET /dashboard
│   ├── models/
│   │   └── models.py         # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py        # Pydantic DTOs
│   └── services/
│       ├── auth_service.py   # JWT + password hashing
│       ├── resume_service.py # PDF parsing (pdfplumber + PyPDF2)
│       ├── ai_service.py # ai scoring + interview Q gen
│       └── ranking_service.py# Rank recomputation engine
├── database/
│   └── db.py                 # SQLAlchemy engine + session
├── uploads/                  # Uploaded resume PDFs
├── seed.py                   # DB seed script
└── .env.example
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login | Login → JWT token |
| POST | /auth/register | Register new user |
| POST | /jobs | Create job posting |
| GET | /jobs | List all jobs |
| POST | /resumes/upload | Upload & parse resume PDF |
| POST | /candidates/screen | AI-score candidate vs job |
| GET | /candidates/rankings | Ranked candidates (filter by job_id) |
| GET | /candidates/{id} | Candidate detail + top score |
| GET | /candidates | List all candidates |
| POST | /interview/questions | Generate AI interview questions |
| POST | /onboarding/create | Create onboarding record |
| GET | /dashboard | Aggregate stats |
