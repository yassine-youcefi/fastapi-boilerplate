from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_auth_service
from app.auth.schemas.auth_schemas import (
    AuthRegisterRequest, AuthRegisterResponse,
    AuthLoginRequest, AuthLoginResponse
)

auth_router = APIRouter()

@auth_router.post(
    "/login",
    response_model=AuthLoginResponse,
    status_code=status.HTTP_200_OK,
    description="Authenticate user and return JWT token and user info.",
    summary="User Login",
)
async def login(login_data: AuthLoginRequest, auth_service=Depends(get_auth_service)):
    return await auth_service.login(login_data=login_data)

@auth_router.post(
    "/signup",
    response_model=AuthRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    description="Register a new user.",
    summary="User Signup",
)
async def signup(signup_data: AuthRegisterRequest, auth_service=Depends(get_auth_service)):
    return await auth_service.signup(signup_data=signup_data)
