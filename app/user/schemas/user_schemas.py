from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from app.config.config import Settings, settings


class AuthSignup(BaseModel):
    full_name: str
    email: EmailStr
    password: str

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


class AuthLogin(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v


class AuthResponse(BaseModel):
    access_token: str
    token_type: str


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

