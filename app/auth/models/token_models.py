from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.integrations.database import Base


class AccessToken(Base):
    """
    SQLAlchemy model for storing JWT access tokens for users.
    """

    __tablename__ = "access_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", backref="access_tokens")
    refresh_tokens = relationship("RefreshToken", back_populates="access_token")

    def __init__(self, *args, **kwargs):
        expires_at = kwargs.get("expires_at")
        if expires_at is None:
            raise ValueError("expires_at must be provided for AccessToken and cannot be None.")
        super().__init__(*args, **kwargs)


class RefreshToken(Base):
    """
    SQLAlchemy model for storing refresh tokens for users.
    """

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    access_token_id = Column(
        Integer,
        ForeignKey("access_tokens.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    token = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", backref="refresh_tokens")
    access_token = relationship("AccessToken", back_populates="refresh_tokens")

    def __init__(self, *args, **kwargs):
        expires_at = kwargs.get("expires_at")
        if expires_at is None:
            raise ValueError("expires_at must be provided for RefreshToken and cannot be None.")
        super().__init__(*args, **kwargs)
