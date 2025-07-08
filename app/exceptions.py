from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from typing import Optional

# Base custom exception for all app-specific errors
class AppBaseException(Exception):
    status_code: int = 400
    error_code: str = "APP_ERROR"
    message: str = "An error occurred."

    def __init__(self, message: Optional[str] = None, error_code: Optional[str] = None, status_code: Optional[int] = None):
        if message:
            self.message = message
        if error_code:
            self.error_code = error_code
        if status_code:
            self.status_code = status_code

# Utility to raise HTTPException with your schema
def raise_http_exception(status_code: int, message: str, error_code: Optional[str] = None):
    raise HTTPException(
        status_code=status_code,
        detail=[{"error_code": error_code, "message": message}]
    )

def raise_predefined_http_exception(exc: Exception):
    raise raise_http_exception(
        status_code=getattr(exc, "status_code", 400),
        message=getattr(exc, "message", str(exc)),
        error_code=getattr(exc, "error_code", "APP_ERROR")
    )

# Centralized custom exception handler
async def custom_http_exception_handler(request: Request, exc: Exception):
    # Handle FastAPI/Starlette HTTPException
    if isinstance(exc, HTTPException):
        detail = exc.detail
        if isinstance(detail, list) and all(isinstance(item, dict) and "message" in item for item in detail):
            return JSONResponse(status_code=exc.status_code, content={"errors": detail})
        return JSONResponse(status_code=exc.status_code, content={"errors": [{"error_code": "HTTP_EXCEPTION", "message": str(detail)}]})
    # Handle custom app exceptions
    if isinstance(exc, AppBaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "errors": [
                    {
                        "error_code": exc.error_code,
                        "message": exc.message
                    }
                ]
            },
        )
    # Fallback for unhandled exceptions
    return JSONResponse(
        status_code=500,
        content={
            "errors": [
                {
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "message": "An internal server error occurred."
                }
            ]
        },
    )

# Custom exception handler for validation errors
async def custom_validation_exception_handler(request: Request, exc: FastAPIRequestValidationError):
    errors = [
        {"error_code": "VALIDATION_ERROR", "message": err["msg"]} for err in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"errors": errors})
