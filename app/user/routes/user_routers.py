from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_auth_service, get_current_user
from app.auth.services.auth_services import AuthService
from app.user.dependencies import get_user_service
from app.user.schemas.user_schemas import UserResponse, UserUpdate
from app.user.services.user_services import UserService

user_router = APIRouter()


@user_router.get(
    "/details",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Get details of the current user from the access token.",
    summary="Get Current User Details",
)
async def get_user_details(current_user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    return current_user


@user_router.put(
    "/update",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Update the current user's information.",
    summary="Update Current User",
)
async def update_user(
    user_update: UserUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    updated_user = await user_service.update_user(user_update, current_user)
    return UserResponse.model_validate(updated_user)


@user_router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete the current user's account. Requires a valid access token in the Authorization header.",
    summary="Delete Current User",
)
async def delete_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    await user_service.delete_user(current_user, auth_service)
    return None
