from fastapi import APIRouter, Depends, status, HTTPException
from app.user.dependencies import get_user_service
from app.user.schemas import UserResponse
from app.user.services.user_services import UserService

user_router = APIRouter()

@user_router.get(
    "/details/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Get details of the user by user_id.",
    summary="Get User Details",
)
async def get_user_details(user_id: int, user_service: UserService = Depends(get_user_service)) -> UserResponse:
    user = await user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=[{"error_code": "NOT_FOUND", "message": f"User with id {user_id} not found."}]
        )
    return user
