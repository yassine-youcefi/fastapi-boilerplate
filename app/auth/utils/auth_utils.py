from typing import Annotated, Union

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services.auth_services import AuthService
from app.config.database import get_db
from app.user.schemas import UserResponse

from .token_utils import TokenUtils

AUTH_PREFIX = "Bearer "


async def get_request_user(
    session: AsyncSession = Depends(get_db),
    authorization: Annotated[Union[str, None], Header()] = None,
) -> UserResponse:

    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if not authorization or not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    payload = await TokenUtils.decode_token(token=authorization.replace(AUTH_PREFIX, "").strip())

    if payload and "user_id" in payload:
        auth_service = AuthService(session=session)
        user = await auth_service.get_user_by_id(user_id=payload["user_id"])
        if user:
            return UserResponse(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                shop_id=getattr(user, "shop_id", None),
            )

    raise auth_exception
