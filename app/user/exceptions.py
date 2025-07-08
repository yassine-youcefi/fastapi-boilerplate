from fastapi import status
from app.exceptions import AppBaseException


class UserNotFoundException(AppBaseException):
    def __init__(self, user_id: int):
        super().__init__(
            message=f"User with ID {user_id} not found",
            error_code="USER_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )
