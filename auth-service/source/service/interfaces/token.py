from abc import abstractmethod

from .base import IService


class ITokenService(IService):
    @abstractmethod
    async def refresh(self, access_token: str) -> str:
        pass
