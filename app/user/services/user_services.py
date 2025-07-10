from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.models.user_models import User
from app.exceptions import raise_predefined_http_exception
from app.user.exceptions import UserNotFoundException
from typing import Optional


class UserService:
    """
    Service class for user-related database operations.
    Handles user lookup, creation, and validation logic.
    """
    def __init__(self, session: AsyncSession) -> None:
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
        result = await self.session.execute(
            select(User).filter_by(email=email)
        )
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
        result = await self.session.execute(
            select(User).filter_by(email=email)
        )
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
        result = await self.session.execute(
            select(User).filter_by(id=user_id)
        )
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
