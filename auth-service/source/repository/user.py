from fastapi import Depends

from database.engine import get_session, AsyncSession
from database.models import User as UserORM
from database.queries.user import (
    create_user, CreateStatus,
    get_user,
    delete_user, DeleteStatus,
)
from utils.hashing import get_hasher, Hasher

from .interfaces.user import IUserRepository, UserCreate, UserResult
from .exceptions import RepositoryError


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession, hasher: Hasher):
        assert isinstance(session, AsyncSession)

        self.__session: AsyncSession = session
        self.__hasher:  Hasher = hasher
    
    async def create(self, user_data: UserCreate) -> UserResult:
        password_hash = await self.__hasher.hash(user_data.password)
        
        user = UserORM(
            username=user_data.username,
            password_hash=password_hash,
        )
        
        status: CreateStatus = await create_user(self.__session, user)

        if status == CreateStatus.Ok:
            return UserResult.model_validate(user)
        
        message = "unexcpected"

        match(status):
            case CreateStatus.AlreadyExists:
                message = "username is already taken"
        
        raise RepositoryError(400, message)
    
    async def get(self, id: int) -> UserResult:
        user = await get_user(self.__session, id, actual=True)

        if user is None:
            raise RepositoryError(404, "user not found")
        
        return UserResult.model_validate(user)

    async def delete(self, id: int) -> None:
        status = await delete_user(self.__session, id)

        if status == DeleteStatus.Ok:
            return
        
        raise RepositoryError(404, "user not found")


def get_user_repo(
        session: AsyncSession = Depends(get_session),
        haser: Hasher = Depends(get_hasher)
    ) -> UserRepository:
    
    return UserRepository(session, haser)
