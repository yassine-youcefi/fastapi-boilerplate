from fastapi import status
from app.exceptions import AppBaseException

class DuplicateUserEmailException(AppBaseException):
    def __init__(self, email: str):
        super().__init__(
            message=f"User with email {email} already exists",
            error_code="DUPLICATE_USER_EMAIL",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class InvalidCredentialsException(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            error_code="INVALID_CREDENTIALS",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
