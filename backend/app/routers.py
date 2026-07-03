import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models import User
from app import schemas, crud, auth

router = APIRouter()

# -----------------
# Authentication
# -----------------
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=user_credentials.email)
    if not user or not auth.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

# -----------------
# Profile
# -----------------
@router.get("/profile", response_model=schemas.UserResponse)
def get_profile(current_user: User = Depends(auth.get_current_active_user)):
    return current_user

@router.put("/profile", response_model=schemas.UserResponse)
def update_profile(profile: schemas.ProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    return crud.update_profile(db, current_user.id, profile)

@router.post("/resume")
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can upload resumes")
    
    os.makedirs("uploads/resumes", exist_ok=True)
    safe_filename = os.path.basename(file.filename.replace("\\", "/"))
    file_path = f"uploads/resumes/{current_user.id}_{safe_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    crud.update_resume(db, current_user.id, file_path)
    return {"filename": file.filename, "file_path": file_path}

# -----------------
# Jobs
# -----------------
@router.get("/jobs", response_model=List[schemas.JobResponse])
def get_all_jobs(db: Session = Depends(get_db)):
    return crud.get_jobs(db)

@router.post("/jobs", response_model=schemas.JobResponse)
def create_new_job(job: schemas.JobCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can create jobs")
    return crud.create_job(db, job, current_user.id)

@router.put("/jobs/{job_id}", response_model=schemas.JobResponse)
def update_existing_job(job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can update jobs")
    job = crud.update_job(db, job_id, job_update, current_user.id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or unauthorized")
    return job

@router.delete("/jobs/{job_id}")
def delete_existing_job(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can delete jobs")
    success = crud.delete_job(db, job_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or unauthorized")
    return {"message": "Job deleted successfully"}

# -----------------
# Applications
# -----------------
@router.post("/jobs/{job_id}/apply", response_model=schemas.ApplicationResponse)
def apply_for_job(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can apply for jobs")
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    application = crud.apply_for_job(db, job_id, current_user.id)
    if not application:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    return application

@router.get("/applications", response_model=List[schemas.ApplicationResponse])
def get_user_applications(db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    return crud.get_applications(db, current_user.id, current_user.role)

@router.patch("/applications/{application_id}", response_model=schemas.ApplicationResponse)
def update_application_status(application_id: int, app_update: schemas.ApplicationUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_active_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can update applications")
    
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Verify the recruiter owns the job for this application
    job = crud.get_job(db, application.job_id)
    if not job or job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this application")
    
    return crud.update_application_status(db, application_id, app_update.status)
