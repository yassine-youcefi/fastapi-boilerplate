from fastapi import status
from typing import Optional, List
from pydantic import BaseModel
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError

# Error Message Schema
class ErrorDetail(BaseModel):
    error_code: Optional[str] = None
    message: str

class ErrorResponse(BaseModel):
    errors: List[ErrorDetail]

# Centralized error handling function
def raise_http_exception(status_code: int, message: str, error_code: Optional[str] = None):
    # Instead of putting errors inside 'detail', put directly in HTTPException.detail
    raise HTTPException(
        status_code=status_code,
        detail=[{"error_code": error_code, "message": message}]
    )

def raise_predefined_http_exception(exc: Exception):
    raise raise_http_exception(
        status_code=exc.status_code,
        message=exc.message,
        error_code=exc.error_code
    )

class DuplicateUserEmailException(Exception):
    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"User with email {email} already exists"
        self.error_code = "DUPLICATE_USER_EMAIL"

class InvalidCredentialsException(Exception):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "Invalid email or password"
        self.error_code = "INVALID_CREDENTIALS"
        
class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f"User with ID {user_id} not found"
        self.error_code = "USER_NOT_FOUND"



# Custom exception handler for HTTPException
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    # If detail is a list of errors, return as {"errors": ...}
    if isinstance(detail, list) and all(isinstance(item, dict) and "message" in item for item in detail):
        return JSONResponse(status_code=exc.status_code, content={"errors": detail})
    # fallback for legacy or non-standard errors
    return JSONResponse(status_code=exc.status_code, content={"errors": [{"message": str(detail)}]})

# Custom exception handler for validation errors
async def custom_validation_exception_handler(request: Request, exc: FastAPIRequestValidationError):
    errors = [
        {"error_code": "VALIDATION_ERROR", "message": err["msg"]} for err in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"errors": errors})
