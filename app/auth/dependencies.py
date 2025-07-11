from typing import Optional

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import AuthenticationRequiredException, InvalidTokenException
from app.auth.services.auth_services import AuthService
from app.auth.utils.token_utils import TokenUtils
from app.config.database import get_db
from app.exceptions import raise_predefined_http_exception
from app.user.models.user_models import User
from app.user.services.user_services import UserService


def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(session=session)


def get_authorization_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise_predefined_http_exception(AuthenticationRequiredException())
    return authorization.split(" ", 1)[1]


async def get_current_user(
    token: str = Depends(get_authorization_token),
    session: AsyncSession = Depends(get_db),
) -> User:
    decoded = await TokenUtils.decode_token(token)
    if not decoded or "user_id" not in decoded:
        raise_predefined_http_exception(InvalidTokenException())
    user_service = UserService(session=session)
    user = await user_service.get_user_by_id(user_id=decoded["user_id"])
    return user
