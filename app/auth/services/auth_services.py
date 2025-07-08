from sqlalchemy.ext.asyncio import AsyncSession
from app.user.models.user_models import User
from app.auth.utils.hash_utils import HashUtils
from app.auth.utils.token_utils import TokenUtils
from app.auth.schemas.auth_schemas import (
    AuthLoginRequest, AuthLoginResponse, AuthSignupRequest, AuthSignupResponse
)
from app.user.schemas import UserResponse
from app.user.services.user_services import UserService
from app.exceptions import raise_predefined_http_exception
from app.auth.exceptions import DuplicateUserEmailException, InvalidCredentialsException
from typing import Any
from app.auth.models.access_token import AccessToken

class AuthService:
    """
    Service class for authentication-related operations such as user signup and login.
    Handles user registration, password hashing, and JWT token generation.
    """
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize AuthService with a database session.
        Args:
            session (AsyncSession): SQLAlchemy async session for database operations.
        """
        self.session = session
        self.user_service = UserService(session)

    async def _generate_token(self, user_id: int) -> str:
        """
        Generate a JWT access token for the user and save it in the database.
        Args:
            user_id (int): The ID of the user for whom to generate the token.
        Returns:
            str: The generated JWT access token.
        """
        token: str = await TokenUtils.generate_token(user_id=user_id)
        access_token_obj = AccessToken(user_id=user_id, token=token)
        self.session.add(access_token_obj)
        await self.session.commit()
        return token

    async def signup(self, signup_data: AuthSignupRequest) -> AuthSignupResponse:
        """
        Register a new user. Hashes the password and saves the user to the database.
        Also saves the generated JWT access token in the database.
        Args:
            signup_data (AuthSignupRequest): The registration data for the new user.
        Returns:
            AuthSignupResponse: The response containing the new user's info.
        Raises:
            DuplicateUserEmailException: If a user with the given email already exists.
        """
        if await self.user_service.user_exists_by_email(email=signup_data.email):
            raise_predefined_http_exception(DuplicateUserEmailException(signup_data.email))
        hashed_password: str = await HashUtils.hash_password(password=signup_data.password)
        signup_data.password = hashed_password
        new_user = User(**signup_data.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        token: str = await self._generate_token(user_id=new_user.id)
        return AuthSignupResponse(
            user=UserResponse(id=new_user.id, full_name=new_user.full_name, email=new_user.email),
            access_token=token,
            token_type="bearer"
        )

    async def login(self, login_data: AuthLoginRequest) -> AuthLoginResponse:
        """
        Authenticate a user and return a JWT token if credentials are valid.
        Also saves the generated JWT access token in the database.
        Args:
            login_data (AuthLoginRequest): The login credentials.
        Returns:
            AuthLoginResponse: The response containing user info and JWT token.
        Raises:
            InvalidCredentialsException: If the credentials are invalid.
        """
        user: User = await self.user_service.get_user_by_email(email=login_data.email)
        if user is None or not await HashUtils.check_password(password=login_data.password, hashed_password=user.password):
            raise_predefined_http_exception(InvalidCredentialsException())
        token: str = await self._generate_token(user_id=user.id)
        return AuthLoginResponse(
            user=UserResponse(id=user.id, full_name=user.full_name, email=user.email),
            access_token=token,
            token_type="bearer"
        )
