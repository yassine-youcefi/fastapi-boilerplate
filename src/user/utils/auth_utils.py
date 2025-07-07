from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Annotated, Union
from .token_utils import TokenUtils
from src.user.services import UserService
from src.user.schemas import UserResponse
from src.database import get_db

AUTH_PREFIX = "Bearer "


def get_request_user(
        session: Session = Depends(get_db),
        authorization: Annotated[Union[str, None], Header()] = None) -> UserResponse:

    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )

    if not authorization or not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    payload = TokenUtils.decode_token(
        token=authorization.replace(AUTH_PREFIX, "").strip())

    if payload and "user_id" in payload:
        user_service = UserService(session=session)
        user = user_service.get_user_by_id(user_id=payload["user_id"])
        if user:
            return UserResponse(id=user.id, full_name=user.full_name, email=user.email, shop_id=user.shop_id)

    raise auth_exception