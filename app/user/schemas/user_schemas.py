from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, description="Full name must contain a space")
    email: Optional[EmailStr] = Field(
        default=None,
        description="User email. Must be a valid email address if provided.",
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v is not None and (not isinstance(v, str) or not v.strip()):
            raise ValueError("Email must be a non-empty string if provided.")
        return v

    class Config:
        from_attributes = True
