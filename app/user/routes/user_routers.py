from fastapi import APIRouter, Depends, status
from app.user.dependencies import get_user_service
from app.user.schemas import (AuthSignup, AuthLogin, AuthResponse, UserResponse,)

user_router = APIRouter()

@user_router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    description="Authenticate user and return JWT token.",
    summary="User Login",
)
async def login(login_data: AuthLogin, user_service=Depends(get_user_service)):
    return await user_service.login(login_data=login_data)


@user_router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    description="Register a new user.",
    summary="User Signup",
)
async def signup(signup_data: AuthSignup, user_service=Depends(get_user_service)):
    return await user_service.signup(signup_data=signup_data)


@user_router.get(
    "/details/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Get details of the user by user_id.",
    summary="Get User Details",
)
async def get_user_details(user_id: int, user_service=Depends(get_user_service)):
    return await user_service.get_user_by_id(user_id=user_id)
