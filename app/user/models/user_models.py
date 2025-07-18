from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.integrations.database import Base

# Association table for many-to-many relationship between User and Role
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): Primary key.
        full_name (str): The user's full name.
        email (str): The user's unique email address.
        password (str): The user's hashed password.
        is_active (bool): Indicates if the user account is active.
        created_at (datetime): The timestamp when the user was created.
        roles (list[Role]): List of roles assigned to the user.
    """

    __tablename__ = "users"
    __table_args__ = {"comment": "Stores user information."}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    # Many-to-many relationship with Role
    roles = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
        lazy="joined",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return (
            f"<User(id={self.id}, email={self.email}, full_name={self.full_name}, "
            f"roles={[role.name for role in self.roles] if self.roles else None})>"
        )


class Role(Base):
    """
    Represents a user role in the system.

    Attributes:
        id (int): Primary key.
        name (str): Unique name of the role.
        permissions (list[str]): Array of permissions associated with the role.
        users (list[User]): List of users assigned this role.
    """

    __tablename__ = "roles"
    __table_args__ = {"comment": "Stores role and permission information."}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    permissions = Column(ARRAY(String), nullable=False)

    # Many-to-many relationship with User
    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
        lazy="select",
    )

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, permissions={self.permissions})>"
