from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.models.application import Application
from app.services.job_service import get_job_by_id

def apply_for_job(db: Session, job_id: int, candidate_id: int) -> Application:
    # Check if job exists
    get_job_by_id(db, job_id)
    
    # Prevent duplicate applications
    existing_app = db.query(Application).filter(
        Application.job_id == job_id,
        Application.candidate_id == candidate_id
    ).first()
    
    if existing_app:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job."
        )
            
    new_application = Application(
        job_id=job_id,
        candidate_id=candidate_id,
        status="pending"
    )
    
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

def get_application_by_id(db: Session, application_id: int) -> Application:
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found."
        )
    return app

def withdraw_application(db: Session, application_id: int, candidate_id: int) -> None:
    app = get_application_by_id(db, application_id)
    
    if app.candidate_id != candidate_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to withdraw this application."
        )
        
    db.delete(app)
    db.commit()

def update_application_status(db: Session, application_id: int, recruiter_id: int, new_status: str) -> Application:
    app = get_application_by_id(db, application_id)
    job = get_job_by_id(db, app.job_id)
    
    if job.recruiter_id != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application."
        )
        
    app.status = new_status
    db.commit()
    db.refresh(app)
    return app

def get_applications_for_candidate(db: Session, candidate_id: int) -> List[Application]:
    return db.query(Application).filter(Application.candidate_id == candidate_id).all()

def get_applications_for_job(db: Session, job_id: int, recruiter_id: int) -> List[Application]:
    # Check if recruiter owns the job
    job = get_job_by_id(db, job_id)
    if job.recruiter_id != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these applications."
        )
        
    return db.query(Application).filter(Application.job_id == job_id).all()
