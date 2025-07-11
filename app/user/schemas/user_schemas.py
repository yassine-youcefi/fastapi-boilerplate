from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, description="Full name must contain a space")
    email: Optional[EmailStr]

    class Config:
        from_attributes = True
