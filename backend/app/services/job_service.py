from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas.job import JobCreate, JobUpdate
from app.models.job import Job

def create_job(db: Session, recruiter_id: int, job_in: JobCreate) -> Job:
    new_job = Job(
        recruiter_id=recruiter_id,
        title=job_in.title,
        description=job_in.description,
        location=job_in.location,
        experience=job_in.experience,
        job_type=job_in.job_type,
        salary=job_in.salary,
        keywords=job_in.keywords
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

def get_job_by_id(db: Session, job_id: int) -> Job:
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found."
        )
    return job

def update_job(db: Session, job_id: int, recruiter_id: int, job_update: JobUpdate) -> Job:
    job = get_job_by_id(db, job_id)
    
    if job.recruiter_id != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job."
        )
        
    update_data = job_update.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        if v is not None:
            setattr(job, k, v)
            
    db.commit()
    db.refresh(job)
    return job

def delete_job(db: Session, job_id: int, recruiter_id: int) -> None:
    job = get_job_by_id(db, job_id)
    
    if job.recruiter_id != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job."
        )
        
    db.delete(job)
    db.commit()

def get_all_jobs(
    db: Session,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    experience: Optional[str] = None,
    job_type: Optional[str] = None,
    salary: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
) -> List[Job]:
    
    query = db.query(Job)
    
    if keyword:
        search_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                Job.title.ilike(search_pattern),
                Job.description.ilike(search_pattern)
            )
        )
        
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
        
    if experience:
        query = query.filter(Job.experience.ilike(f"%{experience}%"))
        
    if job_type:
        query = query.filter(Job.job_type.ilike(f"%{job_type}%"))
        
    if salary:
        query = query.filter(Job.salary.ilike(f"%{salary}%"))
        
    return query.offset(skip).limit(limit).all()

def get_jobs_by_recruiter(db: Session, recruiter_id: int) -> List[Job]:
    return db.query(Job).filter(Job.recruiter_id == recruiter_id).all()
