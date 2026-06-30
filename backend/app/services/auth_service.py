from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.auth import get_password_hash, verify_password

def register_user(db: Session, user_in: UserCreate) -> User:
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
            
    # Create new user
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        profile={}
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def update_user_profile(db: Session, user_id: int, profile_data: dict) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
        
    # Update only the provided fields in the JSON column
    current_profile = dict(user.profile or {})
    for k, v in profile_data.items():
        if v is not None:
            current_profile[k] = v
            
    user.profile = current_profile
    db.commit()
    db.refresh(user)
    return user
