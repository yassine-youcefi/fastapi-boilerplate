from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.config.database import get_db
from app.user.services import UserService
from app.user.schemas import AuthSignup, AuthLogin,  AuthResponse, UserResponse
from app.config.config import Settings, settings


userRouter = APIRouter()


@userRouter.post(
    "/login", 
    status_code=status.HTTP_200_OK, 
    response_model=AuthResponse
)
def login(login_data: AuthLogin, session: Session = Depends(get_db)):
    try:
        user_service = UserService(session=session)
        return user_service.login(login_data=login_data)
    except Exception as e:
        raise e


@userRouter.post(
    "/signup", 
    status_code=status.HTTP_201_CREATED, 
    response_model=UserResponse
)
def signup(signup_data: AuthSignup, session: Session = Depends(get_db)):
    try:
        user_service = UserService(session=session)
        return user_service.signup(signup_data=signup_data)
    except Exception as e:
        raise e
