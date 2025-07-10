import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import (DuplicateUserEmailException,
                                 InvalidCredentialsException,
                                 InvalidTokenException)
from app.auth.models.token_models import AccessToken, RefreshToken
from app.auth.schemas.auth_schemas import (AuthLoginRequest, AuthLoginResponse,
                                           AuthSignupRequest,
                                           AuthSignupResponse,
                                           RefreshTokenRequest,
                                           RefreshTokenResponse)
from app.auth.utils.hash_utils import HashUtils
from app.auth.utils.token_utils import TokenUtils
from app.exceptions import raise_predefined_http_exception
from app.user.models.user_models import User
from app.user.schemas.user_schemas import UserResponse
from app.user.services.user_services import UserService

logger = logging.getLogger(__name__)


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

    async def _generate_tokens(self, user_id: int) -> tuple[str, str]:
        """
        Generate a JWT access token and a refresh token for the user, save both in the database,
        and relate the refresh token to the access token.
        Args:
            user_id (int): The ID of the user for whom to generate the tokens.
        Returns:
            tuple[str, str]: The generated (access_token, refresh_token).
        """
        access_token, access_expires_at = await TokenUtils.generate_access_token(
            user_id=user_id
        )
        logging.debug(
            f"Generated access token for user {user_id}: {access_token}, ----- expires at: {access_expires_at}"
        )
        access_token_obj = AccessToken(
            user_id=user_id,
            token=access_token,
            expires_at=access_expires_at,
        )
        self.session.add(access_token_obj)
        await self.session.flush()

        refresh_token, refresh_expires_at = await TokenUtils.generate_refresh_token(
            user_id=user_id
        )
        refresh_token_obj = RefreshToken(
            user_id=user_id,
            access_token_id=access_token_obj.id,
            token=refresh_token,
            expires_at=refresh_expires_at,
        )
        self.session.add(refresh_token_obj)
        await self.session.commit()
        return access_token, refresh_token

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
            raise_predefined_http_exception(
                DuplicateUserEmailException(signup_data.email)
            )
        hashed_password: str = await HashUtils.hash_password(
            password=signup_data.password
        )
        # Use UserService to create the user
        new_user = await self.user_service.create_user(
            full_name=signup_data.full_name,
            email=signup_data.email,
            password=hashed_password,
        )
        # Extract needed fields before any further session operations
        user_id = new_user.id
        user_email = new_user.email
        user_full_name = new_user.full_name
        access_token, refresh_token = await self._generate_tokens(user_id=user_id)
        return AuthSignupResponse(
            user=UserResponse(id=user_id, full_name=user_full_name, email=user_email),
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
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
        if user is None or not await HashUtils.check_password(
            password=login_data.password, hashed_password=user.password
        ):
            raise_predefined_http_exception(InvalidCredentialsException())
        # Extract needed fields before any further session operations
        user_id = user.id
        user_email = user.email
        user_full_name = user.full_name
        access_token, refresh_token = await self._generate_tokens(user_id=user_id)
        return AuthLoginResponse(
            user=UserResponse(id=user_id, full_name=user_full_name, email=user_email),
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
        )

    async def refresh_token(
        self, refresh_data: RefreshTokenRequest
    ) -> RefreshTokenResponse:
        """
        Validate refresh token, generate new access and refresh tokens, and return them.
        """
        # Find the refresh token in DB
        result = await self.session.execute(
            RefreshToken.__table__.select().where(
                RefreshToken.token == refresh_data.refresh_token
            )
        )
        db_refresh_token = result.fetchone()
        if not db_refresh_token:
            raise_predefined_http_exception(InvalidTokenException())
        # Check expiry
        from datetime import datetime, timezone

        if db_refresh_token.expires_at < datetime.now(timezone.utc):
            # Delete expired token
            await self.session.execute(
                RefreshToken.__table__.delete().where(
                    RefreshToken.token == refresh_data.refresh_token
                )
            )
            await self.session.commit()
            raise_predefined_http_exception(InvalidTokenException())
        # Delete the old refresh token (used or valid)
        await self.session.execute(
            RefreshToken.__table__.delete().where(
                RefreshToken.token == refresh_data.refresh_token
            )
        )
        await self.session.commit()
        # Generate new tokens
        user_id = db_refresh_token.user_id
        access_token, new_refresh_token = await self._generate_tokens(user_id=user_id)
        return RefreshTokenResponse(
            access_token=access_token, refresh_token=new_refresh_token
        )
