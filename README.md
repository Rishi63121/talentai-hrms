TalentAI HRMS

Overview

TalentAI HRMS is a full-stack Human Resource Management System that streamlines recruitment and employee management processes through role-based access control and AI-powered features.

The system provides dedicated dashboards for Admins, Recruiters, and Employees, ensuring secure access to relevant data and functionalities.

⸻

Features

Authentication & Security

* JWT-based Authentication
* Role-Based Access Control (RBAC)
* Secure Password Hashing
* Protected API Endpoints

Admin Module

* Employee Management
* Attendance Management
* Payroll Management
* Performance Review Management
* Analytics Dashboard
* Organization-wide Monitoring

Recruiter Module

* Job Management
* Candidate Management
* Resume Screening
* AI-Powered Interview Question Generation
* Recruitment Workflow Tracking

Employee Module

* Personal Dashboard
* Profile Management
* View Attendance Records
* View Payroll Information
* View Performance Reviews
* Employee-Specific Data Access

⸻

User Roles

Admin

* Manage employees
* Manage attendance records
* Generate payroll
* Manage performance reviews
* View analytics and reports

Recruiter

* Create and manage job postings
* Manage candidates
* Screen resumes
* Generate AI interview questions
* Track recruitment process

Employee

* View personal attendance
* View payroll details
* View performance reviews
* Access profile information

⸻

Technology Stack

Frontend

* React.js
* Tailwind CSS
* Axios
* React Router
* Recharts

Backend

* FastAPI
* SQLAlchemy
* Pydantic
* JWT Authentication

Database

* SQLite

AI Features

* Resume Screening
* Interview Question Generation

⸻

Project Structure

TalentAI-HRMS/
│
├── backend/
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── database/
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── context/
│   │   └── api/
│   │
│   └── public/
│
└── README.md

⸻

Setup Instructions

Backend Setup

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Backend runs on:

http://localhost:8000

Swagger Documentation:

http://localhost:8000/docs

⸻

Frontend Setup

cd frontend
npm install
npm run dev

Frontend runs on:

http://localhost:5173

⸻

API Modules

Authentication

* Login
* Registration
* JWT Token Management

Recruitment

* Jobs
* Candidates
* Resumes
* Interview Generation

HRMS

* Employees
* Attendance
* Payroll
* Performance Reviews

Analytics

* Organization Metrics
* Attendance Insights
* Employee Statistics

⸻

Security Features

* JWT Token Authentication
* Protected Routes
* Employee Data Isolation
* Role-Based Access Control
* Secure Password Storage

⸻

Employee Data Isolation

Employees can only access their own:

* Attendance Records
* Payroll Information
* Performance Reviews
* Profile Details

Administrative users retain access to organization-wide data.

⸻

Demo Accounts

Admin

* Role: Admin

Recruiter

* Role: Recruiter

Employee

* Role: Employee

Passwords have been omitted from the repository for security reasons.

⸻

Future Enhancements

* Email Notifications
* Leave Management
* Employee Self-Service Requests
* AI Candidate Ranking Improvements
* Advanced Analytics Dashboard
* Cloud Deployment

⸻