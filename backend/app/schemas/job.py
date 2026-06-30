from pydantic import BaseModel, Field
from typing import List, Optional

class JobBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    location: str
    experience: str
    job_type: str = Field(..., description="E.g., Full-time, Part-time, Contract")
    salary: str
    keywords: List[str] = []

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    location: Optional[str] = None
    experience: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[str] = None
    keywords: Optional[List[str]] = None

class JobOut(JobBase):
    id: int
    recruiter_id: int

    model_config = {"from_attributes": True}
