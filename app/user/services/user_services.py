from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.models.user_models import User
from app.exceptions import raise_predefined_http_exception
from app.user.exceptions import UserNotFoundException
from typing import Optional


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def user_exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(select(User).filter_by(email=email))
        user: Optional[User] = result.scalars().first()
        return user is not None

    async def get_user_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).filter_by(email=email))
        user: Optional[User] = result.scalars().first()
        if not user:
            raise_predefined_http_exception(UserNotFoundException(user_id=email))
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        user: Optional[User] = result.scalars().first()
        if not user:
            raise_predefined_http_exception(UserNotFoundException(user_id=user_id))
        return user
