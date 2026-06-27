from typing import List, Optional
from fastapi import HTTPException, status
from app.schemas.job import JobCreate, JobUpdate
from app.dummy_data import JOBS, generate_job_id

def create_job(recruiter_id: int, job_in: JobCreate) -> dict:
    new_job = {
        "id": generate_job_id(),
        "recruiter_id": recruiter_id,
        "title": job_in.title,
        "description": job_in.description,
        "location": job_in.location,
        "experience": job_in.experience,
        "job_type": job_in.job_type,
        "salary": job_in.salary,
        "keywords": job_in.keywords
    }
    JOBS.append(new_job)
    return new_job

def get_job_by_id(job_id: int) -> dict:
    for job in JOBS:
        if job["id"] == job_id:
            return job
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Job not found."
    )

def update_job(job_id: int, recruiter_id: int, job_update: JobUpdate) -> dict:
    job = get_job_by_id(job_id)
    
    if job["recruiter_id"] != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job."
        )
        
    update_data = job_update.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        if v is not None:
            job[k] = v
            
    return job

def delete_job(job_id: int, recruiter_id: int) -> None:
    job = get_job_by_id(job_id)
    
    if job["recruiter_id"] != recruiter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job."
        )
        
    JOBS.remove(job)

def get_all_jobs(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    experience: Optional[str] = None,
    job_type: Optional[str] = None,
    salary: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    
    filtered_jobs = JOBS
    
    if keyword:
        keyword_lower = keyword.lower()
        filtered_jobs = [
            j for j in filtered_jobs 
            if keyword_lower in j["title"].lower() or keyword_lower in j["description"].lower()
            or any(keyword_lower in kw.lower() for kw in j["keywords"])
        ]
        
    if location:
        filtered_jobs = [j for j in filtered_jobs if location.lower() in j["location"].lower()]
        
    if experience:
        filtered_jobs = [j for j in filtered_jobs if experience.lower() in j["experience"].lower()]
        
    if job_type:
        filtered_jobs = [j for j in filtered_jobs if job_type.lower() == j["job_type"].lower()]
        
    if salary:
        # A simple string match for salary since it's a string, can be improved to numeric range checking
        filtered_jobs = [j for j in filtered_jobs if salary.lower() in j["salary"].lower()]
        
    return filtered_jobs[skip : skip + limit]

def get_jobs_by_recruiter(recruiter_id: int) -> List[dict]:
    return [job for job in JOBS if job["recruiter_id"] == recruiter_id]
