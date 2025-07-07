from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status
from app.exceptions import raise_http_exception
from app.user.models.user_models import User
from app.user.utils.hash_utils import HashUtils
from app.user.utils.token_utils import TokenUtils
from app.user.schemas import AuthLogin, AuthSignup, AuthResponse


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def signup(self, signup_data: AuthSignup) -> User:
        if await self.user_exist_by_email(email=signup_data.email):
            raise raise_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {signup_data.email} already exists",
                error_code="DUPLICATE_USER_EMAIL"
            )
        hashed_password = HashUtils.hash_password(password=signup_data.password)
        signup_data.password = hashed_password
        new_user = User(**signup_data.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def login(self, login_data: AuthLogin) -> AuthResponse:
        user = await self.get_user_by_email(email=login_data.email)
        if user is None or not HashUtils.check_password(password=login_data.password, hashed_password=user.password):
            raise raise_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                error_code="INVALID_CREDENTIALS"
            )
        token = TokenUtils.generate_token(user_id=user.id)
        return AuthResponse(access_token=token, token_type="bearer")

    async def user_exist_by_email(self, email: str) -> bool:
        result = await self.session.execute(select(User).filter_by(email=email))
        user = result.scalars().first()
        return user is not None

    async def get_user_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).filter_by(email=email))
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        return result.scalars().first()
    
    async def add_shop_to_user(self, user_id: int, shop_id: int) -> User:
        user = await self.get_user_by_id(user_id=user_id)
        user.shop_id = shop_id
        await self.session.commit()
        await self.session.refresh(user)
        return user
