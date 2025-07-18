from typing import Annotated, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import raise_predefined_http_exception
from app.user.exceptions import UserNotFoundException
from app.user.models.user_models import User
from app.user.schemas.user_schemas import UserUpdate


class UserService:
    """
    Service class for user-related database operations.
    Handles user lookup, creation, and validation logic.
    """

    def __init__(self, session: Annotated[AsyncSession, "User DB session"]) -> None:
        """
        Initialize UserService with a database session.
        Args:
            session (AsyncSession): SQLAlchemy async session for database
                operations.
        """
        self.session = session

    async def user_exists_by_email(self, email: str) -> bool:
        """
        Check if a user exists by email.
        Args:
            email (str): The email address to check.
        Returns:
            bool: True if user exists, False otherwise.
        """
        result = await self.session.execute(select(User).filter_by(email=email))
        user: Optional[User] = result.scalars().first()
        return user is not None

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieve a user by email.
        Args:
            email (str): The email address to search for.
        Returns:
            User: The user object if found.
        Raises:
            UserNotFoundException: If no user is found with the given email.
        """
        result = await self.session.execute(select(User).filter_by(email=email))
        user: Optional[User] = result.scalars().first()
        if not user:
            raise_predefined_http_exception(UserNotFoundException(user_id=email))
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by ID.
        Args:
            user_id (int): The user ID to search for.
        Returns:
            User: The user object if found.
        Raises:
            UserNotFoundException: If no user is found with the given ID.
        """
        result = await self.session.execute(select(User).filter_by(id=user_id))
        user: Optional[User] = result.scalars().first()
        if not user:
            raise_predefined_http_exception(UserNotFoundException(user_id=user_id))
        return user

    async def create_user(self, full_name: str, email: str, password: str) -> User:
        """
        Create a new user in the database.
        Args:
            full_name (str): The user's full name.
            email (str): The user's email address.
            password (str): The user's hashed password.
        Returns:
            User: The created user object.
        """
        new_user = User(full_name=full_name, email=email, password=password)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def update_user(self, user_update: UserUpdate, current_user: User) -> User:
        """
        Update an existing user in the database.
        Args:
            user_update (UserUpdate): The user update data (should not contain id or password).
            current_user (User): The current user object.
        Returns:
            User: The updated user object.
        """
        update_data = user_update.dict(exclude_unset=True)
        # Check for email uniqueness if email is being updated
        if "email" in update_data and update_data["email"] != current_user.email:
            if await self.user_exists_by_email(update_data["email"]):
                from app.auth.exceptions import DuplicateUserEmailException

                raise_predefined_http_exception(DuplicateUserEmailException(update_data["email"]))
        for field, value in update_data.items():
            setattr(current_user, field, value)
        await self.session.commit()
        await self.session.refresh(current_user)
        return current_user

    async def delete_user(self, current_user: User, auth_service) -> None:
        """
        Delete the current user from the database, including all related tokens.
        Args:
            current_user (User): The user to delete.
            auth_service (AuthService): The auth service to handle token deletion.
        """
        await auth_service.delete_user_tokens(current_user.id)
        await self.session.delete(current_user)
        await self.session.commit()
