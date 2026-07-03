from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Storing hashed password
    role = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=True)
    resume_path = Column(String(255), nullable=True)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(5000), nullable=False)
    location = Column(String(255))
    salary = Column(String(255))
    experience = Column(String(255))
    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    recruiter = relationship("User")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    status = Column(String(50), default="pending")

    candidate = relationship("User")
    job = relationship("Job")
