from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.user.schemas.user_schemas import UserResponse

user_router = APIRouter()


@user_router.get(
    "/details",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Get details of the current user from the access token.",
    summary="Get Current User Details",
)
async def get_user_details(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return current_user
