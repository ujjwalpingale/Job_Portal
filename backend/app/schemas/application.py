from pydantic import BaseModel, Field
from typing import Literal

class ApplicationBase(BaseModel):
    job_id: int

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationStatusUpdate(BaseModel):
    status: Literal["pending", "accepted", "rejected"] = Field(..., description="New status for the application")

class ApplicationOut(ApplicationBase):
    id: int
    candidate_id: int
    status: str
