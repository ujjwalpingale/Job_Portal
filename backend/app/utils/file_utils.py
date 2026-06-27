import os
import shutil
from fastapi import UploadFile, HTTPException, status
from pathlib import Path

# Base directory for uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_FILE_TYPES = ["application/pdf"]
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def validate_and_save_resume(file: UploadFile, user_id: int) -> str:
    """
    Validates the uploaded resume and saves it to the uploads folder.
    Returns the file path.
    """
    # Validate file type
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    # Note: Fastapi UploadFile doesn't immediately give size, we can read chunks
    # or rely on starlette's Content-Length if provided, but standard practice 
    # without DB is to read the file and check length.
    
    # Save the file
    file_extension = ".pdf"
    file_name = f"resume_user_{user_id}{file_extension}"
    file_path = UPLOAD_DIR / file_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Check size after saving
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE_BYTES:
        os.remove(file_path) # cleanup
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the {MAX_FILE_SIZE_MB}MB limit."
        )

    return str(file_path)
