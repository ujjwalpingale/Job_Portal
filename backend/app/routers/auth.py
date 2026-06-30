from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import register_user, authenticate_user
from app.auth import create_access_token
from app.utils.responses import success_response, error_response
from datetime import timedelta
from app.config import get_settings
from app.dependencies import get_current_user, get_db
from app.models.user import User

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new Candidate or Recruiter.
    """
    user = register_user(db, user_in)
    return success_response(message="User registered successfully", data=user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login endpoint. Returns a JWT access token.
    Uses OAuth2 password flow, meaning username is mapped to email here.
    """
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role
    }

@router.get("/me", response_model=UserOut)
def get_current_logged_in_user(current_user: User = Depends(get_current_user)):
    """
    Get current logged in user details.
    """
    return current_user
