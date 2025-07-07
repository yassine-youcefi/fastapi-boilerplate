from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from app.config.database import get_db
from app.user.services import UserService
from app.user.schemas import AuthSignup, AuthLogin,  AuthResponse, UserResponse


userRouter = APIRouter()


@userRouter.post(
    "/login", 
    status_code=status.HTTP_200_OK, 
    response_model=AuthResponse
)
async def login(login_data: AuthLogin, session: AsyncSession = Depends(get_db)):
    try:
        user_service = UserService(session=session)
        return await user_service.login(login_data=login_data)
    except Exception as e:
        raise e


@userRouter.post(
    "/signup", 
    status_code=status.HTTP_201_CREATED, 
    response_model=UserResponse
)
async def signup(signup_data: AuthSignup, session: AsyncSession = Depends(get_db)):
    try:
        user_service = UserService(session=session)
        return await user_service.signup(signup_data=signup_data)
    except Exception as e:
        raise e
