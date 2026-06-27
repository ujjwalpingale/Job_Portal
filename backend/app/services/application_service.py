from fastapi import HTTPException, status
from typing import List
from app.dummy_data import APPLICATIONS, generate_application_id
from app.services.job_service import get_job_by_id

def apply_for_job(job_id: int, candidate_id: int) -> dict:
    # Check if job exists
    get_job_by_id(job_id)
    
    # Prevent duplicate applications
    for app in APPLICATIONS:
        if app["job_id"] == job_id and app["candidate_id"] == candidate_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied for this job."
            )
            
    new_application = {
        "id": generate_application_id(),
        "job_id": job_id,
        "candidate_id": candidate_id,
        "status": "pending"
    }
    
    APPLICATIONS.append(new_application)
    return new_application

def get_application_by_id(application_id: int) -> dict:
    for app in APPLICATIONS:
        if app["id"] == application_id:
            return app
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Application not found."
    )

def withdraw_application(application_id: int, candidate_id: int) -> None:
    app = get_application_by_id(application_id)
    
    if app["candidate_id"] != candidate_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to withdraw this application."
        )
        
    APPLICATIONS.remove(app)

def update_application_status(application_id: int, recruiter_id: int, new_status: str) -> dict:
    app = get_application_by_id(application_id)
    job = get_job_by_id(app["job_id"])
    
    if job["recruiter_id"] != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application."
        )
        
    app["status"] = new_status
    return app

def get_applications_for_candidate(candidate_id: int) -> List[dict]:
    return [app for app in APPLICATIONS if app["candidate_id"] == candidate_id]

def get_applications_for_job(job_id: int, recruiter_id: int) -> List[dict]:
    # Check if recruiter owns the job
    job = get_job_by_id(job_id)
    if job["recruiter_id"] != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these applications."
        )
        
    return [app for app in APPLICATIONS if app["job_id"] == job_id]
