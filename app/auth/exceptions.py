from fastapi import status
from app.exceptions import AppBaseException

class DuplicateUserEmailException(AppBaseException):
    """
    Exception raised when attempting to register a user with an email that already exists.
    """
    def __init__(self, email: str) -> None:
        """
        Initialize the exception with the duplicate email.
        Args:
            email (str): The duplicate email address.
        """
        super().__init__(
            message=f"User with email {email} already exists",
            error_code="DUPLICATE_USER_EMAIL",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class InvalidCredentialsException(AppBaseException):
    """
    Exception raised when user credentials are invalid during authentication.
    """
    def __init__(self) -> None:
        """
        Initialize the exception for invalid credentials.
        """
        super().__init__(
            message="Invalid email or password",
            error_code="INVALID_CREDENTIALS",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class InvalidTokenException(AppBaseException):
    """
    Exception raised when a token is invalid or cannot be decoded.
    """
    def __init__(self) -> None:
        """
        Initialize the exception for invalid tokens.
        """
        super().__init__(
            message="Invalid or expired token",
            error_code="INVALID_TOKEN",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
