from pydantic import BaseModel, EmailStr, Field

from app.user.schemas.user_schemas import UserResponse


class AuthSignupRequest(BaseModel):
    full_name: str = Field(
        ..., min_length=3, description="Full name must contain a space"
    )
    email: EmailStr
    password: str = Field(
        ..., min_length=8, description="Password must be at least 8 characters"
    )

    class Config:
        orm_mode = True


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ..., min_length=8, description="Password must be at least 8 characters"
    )

    class Config:
        orm_mode = True


class AuthLoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str
    refresh_token: str

    class Config:
        orm_mode = True


class AuthSignupResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str
    refresh_token: str

    class Config:
        orm_mode = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    class Config:
        orm_mode = True


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str

    class Config:
        orm_mode = True
