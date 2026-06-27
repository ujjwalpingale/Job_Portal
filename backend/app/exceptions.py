from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.responses import error_response

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=error_response(message="Something went wrong", errors=[str(exc)])
    )
