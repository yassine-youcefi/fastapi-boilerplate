from typing import Any

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_auth_service
from app.auth.schemas.auth_schemas import (AuthLoginRequest, AuthLoginResponse,
                                           AuthSignupRequest,
                                           AuthSignupResponse,
                                           RefreshTokenRequest,
                                           RefreshTokenResponse)
from app.auth.services.auth_services import AuthService

auth_router = APIRouter()


@auth_router.post(
    "/login",
    response_model=AuthLoginResponse,
    status_code=status.HTTP_200_OK,
    description="Authenticate user and return JWT token and user info.",
    summary="User Login",
)
async def login(
    login_data: AuthLoginRequest, auth_service: AuthService = Depends(get_auth_service)
) -> AuthLoginResponse:
    return await auth_service.login(login_data=login_data)


@auth_router.post(
    "/signup",
    response_model=AuthSignupResponse,
    status_code=status.HTTP_201_CREATED,
    description="Register a new user.",
    summary="User Signup",
)
async def signup(
    signup_data: AuthSignupRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthSignupResponse:
    return await auth_service.signup(signup_data=signup_data)


@auth_router.post(
    "/refresh-token",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    description="Refresh JWT access and refresh tokens.",
    summary="Refresh Token",
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> RefreshTokenResponse:
    return await auth_service.refresh_token(refresh_data=refresh_data)
