import jwt
import time
from starlette.concurrency import run_in_threadpool
from app.config.config import Settings, settings

class TokenUtils:
    @staticmethod
    async def generate_token(user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "expires_in": int(time.time()) + settings.JWT_EXPIRES_IN
        }
        return await run_in_threadpool(
            jwt.encode, payload, settings.JWT_SECRET, settings.JWT_ALGORITHM
        )

    @staticmethod
    async def decode_token(token: str) -> dict:
        try:
            decoded_token = await run_in_threadpool(
                jwt.decode, token, settings.JWT_SECRET, [settings.JWT_ALGORITHM]
            )
            return decoded_token if decoded_token["expires_in"] >= time.time() else None
        except jwt.ExpiredSignatureError:
            print("Token expired")
        except jwt.InvalidTokenError:
            print("Invalid token")
        except Exception as e:
            print(f"Error decoding token: {e}")
        return None

