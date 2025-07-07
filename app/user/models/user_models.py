from app.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.config.config import Settings, settings


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): Primary key.
        full_name (str): The user's full name.
        email (str): The user's unique email address.
        role_id (int): Foreign key linking to the Role table.
        password (str): The user's hashed password.
        is_active (bool): Indicates if the user account is active.
        role (Role): Relationship to the Role model.
    """
    __tablename__ = "users"
    __table_args__ = {"comment": "Stores user information."}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="SET NULL"), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationship with Role
    role = relationship("Role", back_populates="users", lazy="joined")
    
    # Relationship with Shop
    shop = relationship("Shop", back_populates="users", lazy="joined")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name}, role={self.role.name if self.role else None})>"


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

    # Relationship with User
    users = relationship("User", back_populates="role", lazy="select")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, permissions={self.permissions})>"
