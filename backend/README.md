# Job Portal Backend (FastAPI)

This is a professional, production-ready backend for a Job Portal built using **FastAPI**. 
Currently, it uses **in-memory data storage (Python lists/dictionaries)** without any database, keeping the architecture clean and modular so that integrating MySQL and SQLAlchemy later will require minimal changes.

## Features

- **JWT Authentication** for Candidates and Recruiters.
- **Role-Based Authorization** protecting respective endpoints.
- **Candidate Endpoints**: Register, Profile update, Resume Upload, Job Applications.
- **Recruiter Endpoints**: Register, Profile update, Post/Update/Delete Jobs, View applicants, Change Application Status.
- **Public Endpoints**: View Jobs, Search and Filter Jobs (by keyword, location, experience, etc.).
- **Middleware**: CORS, Request Processing Time, and Logging.
- **Global Exception Handling**: Standardized JSON responses for Success/Errors.

## Tech Stack

- **Python 3.12+**
- **FastAPI**
- **Pydantic v2**
- **JWT (python-jose)**
- **Bcrypt (passlib)**
- **Uvicorn**

## Project Structure

```text
backend/
├── app/
│   ├── routers/       # API endpoints (auth, candidate, recruiter, jobs, applications)
│   ├── schemas/       # Pydantic models for request/response validation
│   ├── services/      # Business logic and in-memory data manipulation
│   ├── utils/         # Helper functions (responses, file uploads)
│   ├── dependencies.py# FastAPI dependencies (auth, roles)
│   ├── auth.py        # Password hashing and JWT generation
│   ├── config.py      # Environment variables configuration
│   ├── exceptions.py  # Global exception handlers
│   ├── dummy_data.py  # In-memory storage (USERS, JOBS, APPLICATIONS)
│   ├── middleware.py  # Custom middleware
│   └── main.py        # Application entry point
├── uploads/           # Uploaded resumes (PDFs)
├── requirements.txt
└── .env
```

## Running the Application

1. Create a virtual environment and activate it.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Open Swagger UI to explore and test the endpoints:
   - **http://127.0.0.1:8000/docs**
