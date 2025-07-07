from bcrypt import checkpw, hashpw, gensalt
from starlette.concurrency import run_in_threadpool


class HashUtils:
    @staticmethod
    async def check_password(password: str, hashed_password: str) -> bool:
        return await run_in_threadpool(
            checkpw, password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @staticmethod
    async def hash_password(password: str) -> str:
        hashed = await run_in_threadpool(
            hashpw, password.encode("utf-8"), gensalt()
        )
        return hashed.decode("utf-8")
