from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models.user_models import User
from app.user.utils.hash_utils import HashUtils
from app.user.utils.token_utils import TokenUtils
from app.user.schemas import AuthLogin, AuthSignup, AuthResponse
from app.user.exceptions import raise_predefined_http_exception, DuplicateUserEmailException, InvalidCredentialsException, UserNotFoundException


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def signup(self, signup_data: AuthSignup) -> User:
        if await self.user_exists_by_email(email=signup_data.email):
            raise_predefined_http_exception(DuplicateUserEmailException(signup_data.email))
        hashed_password = await HashUtils.hash_password(password=signup_data.password)
        signup_data.password = hashed_password
        new_user = User(**signup_data.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def login(self, login_data: AuthLogin) -> AuthResponse:
        user = await self.get_user_by_email(email=login_data.email)
        if user is None or not await HashUtils.check_password(password=login_data.password, hashed_password=user.password):
            raise_predefined_http_exception(InvalidCredentialsException())
        token = await TokenUtils.generate_token(user_id=user.id)
        return AuthResponse(access_token=token, token_type="bearer")

    async def user_exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(select(User).filter_by(email=email))
        user = result.scalars().first()
        return user is not None

    async def get_user_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).filter_by(email=email))
        user = result.scalars().first()
        if not user:
            raise_predefined_http_exception(UserNotFoundException(user_id=email))
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        user = result.scalars().first()
        if not user:
            raise_predefined_http_exception(UserNotFoundException(user_id=user_id))
        return user
