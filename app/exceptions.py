from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException
from app.config.config import Settings, settings

# Error Message Schema
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

# Centralized error handling function
def raise_http_exception(status_code: int, detail: str, error_code: Optional[str] = None):
    raise HTTPException(
        status_code=status_code,
        detail={"detail": detail, "error_code": error_code}
    )