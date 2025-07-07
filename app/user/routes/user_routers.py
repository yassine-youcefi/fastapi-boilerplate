from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from app.config.database import get_db
from app.user.dependencies import get_user_service
from app.user.schemas import AuthSignup, AuthLogin,  AuthResponse, UserResponse


userRouter = APIRouter()


@userRouter.post(
    "/login", 
    status_code=status.HTTP_200_OK, 
    response_model=AuthResponse
)
async def login(login_data: AuthLogin, user_service=Depends(get_user_service)):
    return await user_service.login(login_data=login_data)


@userRouter.post(
    "/signup", 
    status_code=status.HTTP_201_CREATED, 
    response_model=UserResponse
)
async def signup(signup_data: AuthSignup, user_service=Depends(get_user_service)):
    return await user_service.signup(signup_data=signup_data)
