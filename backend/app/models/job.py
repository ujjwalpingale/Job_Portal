from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(5000), nullable=False)
    location = Column(String(255))
    experience = Column(String(255))
    job_type = Column(String(255))
    salary = Column(String(255))
    keywords = Column(JSON, default=[])
