from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr


class UserUpdate(BaseModel):
    id: int
    full_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    @validator("full_name")
    def full_name_must_contain_space(cls, v):
        if " " not in v:
            raise ValueError("full_name must contain a space")
        return v

    @validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v

