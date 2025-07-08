from pydantic import BaseModel, EmailStr, validator
from app.user.schemas.user_schemas import UserResponse

class AuthSignupRequest(BaseModel):
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

class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v

class AuthLoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str
    refresh_token: str

class AuthSignupResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str
    refresh_token: str
