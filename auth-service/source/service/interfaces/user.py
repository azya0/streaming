from abc import ABC, abstractmethod

from scheme.request import User as UserCreate, UserAuth
from scheme.response import User as UserResult, Tokens


class IUserService(ABC):
    @abstractmethod
    async def create(self, user_data: UserCreate) -> UserResult:
        pass
    
    @abstractmethod
    async def get(self, id: int) -> UserResult | None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> UserResult | None:
        pass

    @abstractmethod
    async def login(self, user_data: UserAuth) -> Tokens:
        pass