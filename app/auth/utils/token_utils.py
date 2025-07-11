import logging
import secrets
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple

import jwt
import pytz
from starlette.concurrency import run_in_threadpool

from app.config.config import settings


class TokenUtils:

    @staticmethod
    async def decode_token(token: str) -> Optional[dict]:
        """
        Decode and validate a JWT token. Returns the decoded payload if valid and not expired, else None.
        """
        try:
            decoded_token = await run_in_threadpool(
                jwt.decode,
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
                options={"require": ["exp"]},
            )
            return decoded_token
        except jwt.ExpiredSignatureError:
            logging.warning("Token expired")
        except jwt.InvalidTokenError:
            logging.warning("Invalid token")
        except Exception as e:
            logging.error(f"Error decoding token: {e}")
        return None

    @staticmethod
    async def generate_access_token(user_id: int) -> Tuple[str, datetime]:
        """
        Generate a JWT access token for the given user ID and return the token and its expiry as a datetime.
        Args:
            user_id (int): The user ID for whom the token is generated.
        Returns:
            Tuple[str, datetime]: The generated JWT access token and its expiry datetime (Dubai timezone).
        """
        dubai_tz = pytz.timezone("Asia/Dubai")
        expires_at_ts = int(time.time()) + settings.JWT_ACCESS_EXPIRES_IN
        payload = {"user_id": user_id, "exp": expires_at_ts, "iat": int(time.time())}
        token = await run_in_threadpool(jwt.encode, payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        expires_at_dubai = datetime.fromtimestamp(expires_at_ts, tz=dubai_tz)
        return token, expires_at_dubai

    @staticmethod
    async def generate_refresh_token(user_id: int, expires_in: int = None) -> Tuple[str, datetime]:
        """
        Generate a secure random refresh token and its expiry datetime.
        Args:
            user_id (int): The user ID for whom the token is generated.
            expires_in (int, optional): Expiry in seconds. Defaults to settings.JWT_REFRESH_EXPIRES_IN.
        Returns:
            Tuple[str, datetime]: The refresh token and its expiry datetime (Dubai timezone).
        """
        dubai_tz = pytz.timezone("Asia/Dubai")
        if expires_in is None:
            expires_in = settings.JWT_REFRESH_EXPIRES_IN
        token = secrets.token_urlsafe(64)
        expires_at_dubai = datetime.now(dubai_tz) + timedelta(seconds=expires_in)
        return token, expires_at_dubai
