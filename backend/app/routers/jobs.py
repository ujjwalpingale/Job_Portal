from fastapi import APIRouter, Query
from typing import Optional
from app.services.job_service import get_all_jobs, get_job_by_id
from app.utils.responses import success_response

router = APIRouter(prefix="/jobs", tags=["Public Jobs"])

@router.get("")
def search_and_filter_jobs(
    keyword: Optional[str] = Query(None, description="Search by title, description or keywords"),
    location: Optional[str] = Query(None, description="Filter by location"),
    experience: Optional[str] = Query(None, description="Filter by experience level"),
    job_type: Optional[str] = Query(None, description="Filter by job type"),
    salary: Optional[str] = Query(None, description="Filter by salary string"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get all jobs, search and filter. Publicly accessible.
    """
    jobs = get_all_jobs(
        keyword=keyword,
        location=location,
        experience=experience,
        job_type=job_type,
        salary=salary,
        skip=skip,
        limit=limit
    )
    return success_response(message="Jobs retrieved successfully", data=jobs)

@router.get("/{job_id}")
def get_job_details(job_id: int):
    """
    Get details of a specific job. Publicly accessible.
    """
    job = get_job_by_id(job_id)
    return success_response(message="Job details retrieved successfully", data=job)
