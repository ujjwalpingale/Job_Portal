from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import RecruiterProfileUpdate, UserOut
from app.schemas.job import JobCreate, JobUpdate, JobOut
from app.schemas.application import ApplicationStatusUpdate
from app.dependencies import get_current_user, RoleChecker, get_db
from app.services.auth_service import update_user_profile
from app.services.job_service import create_job, update_job, delete_job, get_jobs_by_recruiter
from app.services.application_service import get_applications_for_job, update_application_status
from app.utils.responses import success_response
from app.models.user import User

router = APIRouter(prefix="/recruiter", tags=["Recruiter"])
allow_recruiter = RoleChecker(["recruiter"])

@router.get("/profile", response_model=UserOut)
def view_company_profile(current_user: User = Depends(allow_recruiter)):
    """View company profile."""
    return current_user

@router.put("/profile")
def update_company_profile(
    profile_data: RecruiterProfileUpdate, 
    current_user: User = Depends(allow_recruiter),
    db: Session = Depends(get_db)
):
    """Update company profile."""
    updated_user = update_user_profile(db, current_user.id, profile_data.model_dump(exclude_unset=True))
    return success_response(message="Company profile updated successfully", data=updated_user)

@router.post("/jobs", response_model=dict)
def post_job(
    job_in: JobCreate, 
    current_user: User = Depends(allow_recruiter),
    db: Session = Depends(get_db)
):
    """Create a new job posting."""
    job = create_job(db, current_user.id, job_in)
    return success_response(message="Job created successfully", data=job)

@router.put("/jobs/{job_id}", response_model=dict)
def edit_job(
    job_id: int, 
    job_in: JobUpdate, 
    current_user: User = Depends(allow_recruiter),
    db: Session = Depends(get_db)
):
    """Update a job posting."""
    job = update_job(db, job_id, current_user.id, job_in)
    return success_response(message="Job updated successfully", data=job)

@router.delete("/jobs/{job_id}", response_model=dict)
def remove_job(
    job_id: int, 
    current_user: User = Depends(allow_recruiter),
    db: Session = Depends(get_db)
):
    """Delete a job posting."""
    delete_job(db, job_id, current_user.id)
    return success_response(message="Job deleted successfully")

@router.get("/jobs", response_model=dict)
def view_own_jobs(
    current_user: User = Depends(allow_recruiter),
    db: Session = Depends(get_db)
):
    """View all jobs posted by the recruiter."""
    jobs = get_jobs_by_recruiter(db, current_user.id)
    return success_response(message="Jobs retrieved successfully", data=jobs)

@router.get("/jobs/{job_id}/applicants", response_model=dict)
def view_applicants(
    job_id: int, 
    current_user: User = Depends(allow_recruiter),
    db: Session = Depends(get_db)
):
    """View all applicants for a specific job."""
    applications = get_applications_for_job(db, job_id, current_user.id)
    return success_response(message="Applicants retrieved successfully", data=applications)

@router.put("/applications/{application_id}/status", response_model=dict)
def change_application_status(
    application_id: int, 
    status_update: ApplicationStatusUpdate, 
    current_user: User = Depends(allow_recruiter),
    db: Session = Depends(get_db)
):
    """Change the status of an application (e.g., pending, accepted, rejected)."""
    app = update_application_status(db, application_id, current_user.id, status_update.status)
    return success_response(message="Application status updated successfully", data=app)
