from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(50), default="pending")
