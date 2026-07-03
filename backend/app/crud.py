from sqlalchemy.orm import Session
from app.models import User, Job, Application
from app.schemas import UserCreate, JobCreate, JobUpdate, ProfileUpdate
from app.auth import get_password_hash

# -----------------
# User CRUD
# -----------------
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_profile(db: Session, user_id: int, profile: ProfileUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if profile.name is not None:
            db_user.name = profile.name
        if profile.phone is not None:
            db_user.phone = profile.phone
        db.commit()
        db.refresh(db_user)
    return db_user

def update_resume(db: Session, user_id: int, file_path: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.resume_path = file_path
        db.commit()
        db.refresh(db_user)
    return db_user

# -----------------
# Job CRUD
# -----------------
def create_job(db: Session, job: JobCreate, recruiter_id: int):
    db_job = Job(
        title=job.title,
        description=job.description,
        location=job.location,
        salary=job.salary,
        experience=job.experience,
        recruiter_id=recruiter_id
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session):
    return db.query(Job).all()

def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()

def update_job(db: Session, job_id: int, job_update: JobUpdate, recruiter_id: int):
    db_job = db.query(Job).filter(Job.id == job_id, Job.recruiter_id == recruiter_id).first()
    if db_job:
        for key, value in job_update.model_dump(exclude_unset=True).items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int, recruiter_id: int):
    db_job = db.query(Job).filter(Job.id == job_id, Job.recruiter_id == recruiter_id).first()
    if db_job:
        # Delete related applications first to prevent IntegrityError
        db.query(Application).filter(Application.job_id == job_id).delete(synchronize_session=False)
        db.delete(db_job)
        db.commit()
        return True
    return False

# -----------------
# Application CRUD
# -----------------
def apply_for_job(db: Session, job_id: int, candidate_id: int):
    # Check if already applied
    existing_application = db.query(Application).filter(
        Application.job_id == job_id,
        Application.candidate_id == candidate_id
    ).first()
    if existing_application:
        return None
    
    db_app = Application(job_id=job_id, candidate_id=candidate_id, status="pending")
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_applications(db: Session, user_id: int, role: str):
    if role == "candidate":
        return db.query(Application).filter(Application.candidate_id == user_id).all()
    elif role == "recruiter":
        # Get all jobs posted by this recruiter
        return db.query(Application).join(Job).filter(Job.recruiter_id == user_id).all()
    return []

def get_application(db: Session, app_id: int):
    return db.query(Application).filter(Application.id == app_id).first()

def update_application_status(db: Session, app_id: int, status: str):
    db_app = db.query(Application).filter(Application.id == app_id).first()
    if db_app:
        db_app.status = status
        db.commit()
        db.refresh(db_app)
    return db_app
