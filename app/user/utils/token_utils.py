import jwt
import time 
from app.config import settings

class TokenUtils:
    @staticmethod
    def generate_token(user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "expires_in": int(time.time()) + settings.JWT_EXPIRES_IN
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return decoded_token if decoded_token["expires_in"] >= time.time() else None
        except:
            print("Error decoding token")
            return None
        
