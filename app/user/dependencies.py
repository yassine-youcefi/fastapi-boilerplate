from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.user.services.user_services import UserService


def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session=session)
