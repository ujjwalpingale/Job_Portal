from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: str = Field(..., description="Must be 'candidate' or 'recruiter'")
    
    @field_validator('password')
    def password_strength(cls, v):
        # Basic validation for strong password
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
        return v
    
    @field_validator('role')
    def validate_role(cls, v):
        if v not in ("candidate", "recruiter"):
            raise ValueError("Role must be 'candidate' or 'recruiter'.")
        return v

class CandidateProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[list[str]] = None
    resume_url: Optional[str] = None
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r"^\+?1?\d{9,15}$", v):
            raise ValueError("Invalid phone number format.")
        return v

class RecruiterProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    company_website: Optional[str] = None
    company_description: Optional[str] = None

class UserOut(UserBase):
    id: int
    role: str
    profile: dict
