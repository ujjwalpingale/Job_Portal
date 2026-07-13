from pydantic import BaseModel, EmailStr
from typing import Optional, List

# -----------------
# User Schemas
# -----------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    phone: Optional[str] = None
    resume_path: Optional[str] = None

    class Config:
        from_attributes = True

# -----------------
# Job Schemas
# -----------------
class JobCreate(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    location: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    recruiter_id: int

    class Config:
        from_attributes = True

# -----------------
# Application Schemas
# -----------------
class CandidateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    resume_path: Optional[str] = None

    class Config:
        from_attributes = True

class ApplicationResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    status: str
    candidate: Optional[CandidateResponse] = None

    class Config:
        from_attributes = True

class ApplicationUpdate(BaseModel):
    status: str
