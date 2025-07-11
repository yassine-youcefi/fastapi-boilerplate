from pydantic import BaseModel, EmailStr, Field

from app.user.schemas.user_schemas import UserResponse


class AuthSignupRequest(BaseModel):
    full_name: str = Field(..., min_length=3, description="Full name must contain a space")
    email: EmailStr = Field(..., description="User email. Must be a valid, non-empty email address.")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()
        yield cls.validate_email

    @classmethod
    def validate_email(cls, v):
        if not v or not isinstance(v, str) or not v.strip():
            raise ValueError("Email must be a non-empty string.")
        return v

    class Config:
        from_attributes = True


class AuthLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email. Must be a valid, non-empty email address.")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()
        yield cls.validate_email

    @classmethod
    def validate_email(cls, v):
        if not v or not isinstance(v, str) or not v.strip():
            raise ValueError("Email must be a non-empty string.")
        return v

    class Config:
        from_attributes = True


class AuthLoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str
    refresh_token: str

    class Config:
        from_attributes = True


class AuthSignupResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str
    refresh_token: str

    class Config:
        from_attributes = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str

    class Config:
        from_attributes = True
