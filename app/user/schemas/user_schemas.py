from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    full_name: Optional[str] = Field(None, min_length=3, description="Full name must contain a space")
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=8, description="Password must be at least 8 characters")

    class Config:
        orm_mode = True

