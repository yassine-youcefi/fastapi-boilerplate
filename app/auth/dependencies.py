from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services.auth_services import AuthService
from app.config.database import get_db


def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(session=session)
