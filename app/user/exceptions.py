from fastapi import status
from app.exceptions import AppBaseException


class UserNotFoundException(AppBaseException):
    """
    Exception raised when a user is not found in the database.
    """

    def __init__(self, user_id: int) -> None:
        """
        Initialize the exception with the missing user's ID.
        Args:
            user_id (int): The ID of the user that was not found.
        """
        super().__init__(
            message=f"User with ID {user_id} not found",
            error_code="USER_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )
