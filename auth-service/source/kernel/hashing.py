from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from settings import ProgramConstants


class Hasher:
    def __init__(self):
        settings = ProgramConstants()

        self.hasher = PasswordHasher()
        self.pool = ThreadPoolExecutor(
            max_workers=settings.HASH_WORKERS_NUM
        )

    async def hash(self, data: str) -> str:
        return await get_event_loop().run_in_executor(
            self.pool,
            self.hasher.hash,
            data
        )

    async def verify(self, hash: str, data: str) -> bool:
        try:
            await get_event_loop().run_in_executor(
                self.pool,
                self.hasher.verify,
                hash,
                data
            )
        except VerifyMismatchError:
            return False
        
        return True


@lru_cache
def get_hasher() -> Hasher:
    return Hasher()
