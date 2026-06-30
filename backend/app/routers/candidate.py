from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.user import CandidateProfileUpdate, UserOut
from app.dependencies import get_current_user, RoleChecker, get_db
from app.services.auth_service import update_user_profile
from app.services.application_service import get_applications_for_candidate
from app.utils.file_utils import validate_and_save_resume
from app.utils.responses import success_response
from app.models.user import User

router = APIRouter(prefix="/candidate", tags=["Candidate"])
allow_candidate = RoleChecker(["candidate"])

@router.get("/profile", response_model=UserOut)
def view_profile(current_user: User = Depends(allow_candidate)):
    """View candidate profile."""
    return current_user

@router.put("/profile")
def update_profile(
    profile_data: CandidateProfileUpdate, 
    current_user: User = Depends(allow_candidate),
    db: Session = Depends(get_db)
):
    """Update candidate profile."""
    updated_user = update_user_profile(db, current_user.id, profile_data.model_dump(exclude_unset=True))
    return success_response(message="Profile updated successfully", data=updated_user)

@router.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...), 
    current_user: User = Depends(allow_candidate),
    db: Session = Depends(get_db)
):
    """Upload resume (PDF only, max 5MB)."""
    file_path = validate_and_save_resume(file, current_user.id)
    
    # Update user's profile with resume url
    updated_user = update_user_profile(db, current_user.id, {"resume_url": file_path})
    
    return success_response(message="Resume uploaded successfully", data={"resume_url": file_path})

@router.get("/applications")
def view_applied_jobs(current_user: User = Depends(allow_candidate), db: Session = Depends(get_db)):
    """View all jobs applied to by the candidate."""
    applications = get_applications_for_candidate(db, current_user.id)
    return success_response(message="Applications retrieved successfully", data=applications)
