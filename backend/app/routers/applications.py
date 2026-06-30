from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.application import ApplicationCreate
from app.dependencies import get_current_user, RoleChecker, get_db
from app.services.application_service import apply_for_job, withdraw_application, get_applications_for_candidate
from app.utils.responses import success_response
from app.models.user import User

router = APIRouter(prefix="/applications", tags=["Applications"])
allow_candidate = RoleChecker(["candidate"])

@router.post("", response_model=dict)
def apply_job(
    app_in: ApplicationCreate, 
    current_user: User = Depends(allow_candidate),
    db: Session = Depends(get_db)
):
    """Apply for a job."""
    application = apply_for_job(db, app_in.job_id, current_user.id)
    return success_response(message="Successfully applied for job", data=application)

@router.get("", response_model=dict)
def view_my_applications(
    current_user: User = Depends(allow_candidate),
    db: Session = Depends(get_db)
):
    """View my applications."""
    applications = get_applications_for_candidate(db, current_user.id)
    return success_response(message="Applications retrieved successfully", data=applications)

@router.delete("/{application_id}", response_model=dict)
def withdraw_my_application(
    application_id: int, 
    current_user: User = Depends(allow_candidate),
    db: Session = Depends(get_db)
):
    """Withdraw an application."""
    withdraw_application(db, application_id, current_user.id)
    return success_response(message="Application withdrawn successfully")
