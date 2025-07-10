from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from starlette.concurrency import run_in_threadpool

ph = PasswordHasher()

class HashUtils:
    @staticmethod
    async def check_password(password: str, hashed_password: str) -> bool:
        try:
            return await run_in_threadpool(ph.verify, hashed_password, password)
        except VerifyMismatchError:
            return False

    @staticmethod
    async def hash_password(password: str) -> str:
        return await run_in_threadpool(ph.hash, password)
