from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.middleware import ProcessTimeMiddleware
from app.exceptions import global_exception_handler
from app.routers import auth, candidate, recruiter, jobs, applications

from app.database import engine, Base
from app.models import user, job, application

# Create tables
Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A professional, production-ready backend for a Job Portal using FastAPI (MySQL Data version).",
    version="1.0.0",
)

# Add custom middlewares
app.add_middleware(ProcessTimeMiddleware)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update with frontend URLs in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add global exception handlers
app.add_exception_handler(Exception, global_exception_handler)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(candidate.router, prefix=settings.API_V1_STR)
app.include_router(recruiter.router, prefix=settings.API_V1_STR)
app.include_router(jobs.router, prefix=settings.API_V1_STR)
app.include_router(applications.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}!"}

