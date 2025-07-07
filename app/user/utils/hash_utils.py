from bcrypt import checkpw, hashpw, gensalt
from app.config.config import Settings, settings


class HashUtils:
    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def hash_password(password: str) -> str:
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
