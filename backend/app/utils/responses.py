from typing import Any, Optional, Dict
from pydantic import BaseModel

class APIResponse(BaseModel):
    """
    Standard API Response model.
    """
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[list] = None

def success_response(message: str, data: Any = None) -> dict:
    """
    Returns a standard success response.
    """
    return {
        "success": True,
        "message": message,
        "data": data or {}
    }

def error_response(message: str, errors: list = None) -> dict:
    """
    Returns a standard error response.
    """
    return {
        "success": False,
        "message": message,
        "errors": errors or []
    }
