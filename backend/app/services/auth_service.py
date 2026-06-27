from fastapi import HTTPException, status
from app.schemas.user import UserCreate
from app.dummy_data import USERS, generate_user_id
from app.auth import get_password_hash, verify_password

def register_user(user_in: UserCreate) -> dict:
    # Check if user already exists
    for u in USERS:
        if u["email"] == user_in.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
            
    # Create new user
    new_user = {
        "id": generate_user_id(),
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
        "role": user_in.role,
        "profile": {}
    }
    
    USERS.append(new_user)
    
    # Return user without password
    return {
        "id": new_user["id"],
        "email": new_user["email"],
        "role": new_user["role"],
        "profile": new_user["profile"]
    }

def authenticate_user(email: str, password: str) -> dict:
    for user in USERS:
        if user["email"] == email:
            if verify_password(password, user["hashed_password"]):
                return user
    return None

def get_user_by_id(user_id: int) -> dict:
    for user in USERS:
        if user["id"] == user_id:
            return user
    return None

def update_user_profile(user_id: int, profile_data: dict) -> dict:
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
        
    # Update only the provided fields
    for k, v in profile_data.items():
        if v is not None:
            user["profile"][k] = v
            
    return {
        "id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "profile": user["profile"]
    }
