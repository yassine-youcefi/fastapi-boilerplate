import jwt
import time
import secrets
from typing import Tuple
from datetime import datetime, timedelta, timezone
from starlette.concurrency import run_in_threadpool
from app.config.config import settings
import pytz


class TokenUtils:

    @staticmethod
    async def decode_token(token: str) -> dict:
        try:
            decoded_token = await run_in_threadpool(
                jwt.decode, token, settings.JWT_SECRET, [
                    settings.JWT_ALGORITHM]
            )
            return decoded_token if decoded_token["expires_at"] >= time.time() else None
        except jwt.ExpiredSignatureError:
            print("Token expired")
        except jwt.InvalidTokenError:
            print("Invalid token")
        except Exception as e:
            print(f"Error decoding token: {e}")
        return None

    @staticmethod
    async def generate_access_token(user_id: int) -> Tuple[str, datetime]:
        """
        Generate a JWT access token for the given user ID and return the token and its expiry as a datetime.
        Args:
            user_id (int): The user ID for whom the token is generated.
        Returns:
            Tuple[str, datetime]: The generated JWT access token and its expiry datetime.
        """
        expires_at_ts = int(time.time()) + settings.JWT_ACCESS_EXPIRES_IN
        payload = {
            "user_id": user_id,
            "expires_at": expires_at_ts
        }
        token = await run_in_threadpool(
            jwt.encode, payload, settings.JWT_SECRET, settings.JWT_ALGORITHM
        )

        expires_at = datetime.fromtimestamp(expires_at_ts, tz=pytz.timezone('Asia/Dubai'))
        # Convert to UTC before saving to DB
        expires_at_utc = expires_at.astimezone(timezone.utc)
        return token, expires_at_utc

    @staticmethod
    async def generate_refresh_token(user_id: int, expires_in: int = None) -> Tuple[str, datetime]:
        """
        Generate a secure random refresh token and its expiry datetime.
        Args:
            user_id (int): The user ID for whom the token is generated.
            expires_in (int, optional): Expiry in seconds. Defaults to settings.JWT_REFRESH_EXPIRES_IN.
        Returns:
            Tuple[str, datetime]: The refresh token and its expiry datetime.
        """
        if expires_in is None:
            expires_in = settings.JWT_REFRESH_EXPIRES_IN
        token = secrets.token_urlsafe(64)
        expires_at = datetime.now(pytz.timezone('Asia/Dubai')) + timedelta(seconds=expires_in)
        # Convert to UTC before saving to DB
        expires_at_utc = expires_at.astimezone(timezone.utc)
        return token, expires_at_utc
