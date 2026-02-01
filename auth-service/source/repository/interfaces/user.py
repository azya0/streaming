from abc import ABC, abstractmethod

from scheme.request import User as UserCreate
from scheme.response import User as UserResult


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user_data: UserCreate) -> UserResult:
        pass
    
    @abstractmethod
    async def get(self, id: int) -> UserResult | None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> UserResult | None:
        pass
