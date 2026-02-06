from fastapi import Depends

from database.engine import get_session, AsyncSession
from database.models import User as UserORM
from database.queries.user import (
    create_user, CreateStatus,
    get_user,
    delete_user, DeleteStatus,
    get_user_by_username,
)
from kernel.hashing import get_hasher, Hasher
from kernel.tokens import get_token_logic, TokenLogic

from .interfaces.user import IUserService, UserCreate, UserResult, UserAuth, Tokens
from .exceptions import ServiceError


class UserService(IUserService):
    def __init__(self, session: AsyncSession, hasher: Hasher, token_logic: TokenLogic):
        assert isinstance(session, AsyncSession)

        self.__session: AsyncSession = session
        self.__hasher:  Hasher = hasher
        self.__token:   TokenLogic = token_logic
    
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
        
        raise ServiceError(400, message)
    
    async def get(self, id: int) -> UserResult:
        user = await get_user(self.__session, id, actual=True)

        if user is None:
            raise ServiceError(404, "user not found")
        
        return UserResult.model_validate(user)

    async def delete(self, id: int) -> None:
        status = await delete_user(self.__session, id)

        if status == DeleteStatus.Ok:
            return
        
        raise ServiceError(404, "user not found")
    
    async def login(self, user_data: UserAuth) -> Tokens:
        user: UserORM | None = await get_user_by_username(self.__session, user_data.username)

        if user is None:
            raise ServiceError(404, "user not found")

        if not await self.__hasher.verify(user.password_hash, user_data.password):
            raise ServiceError(400, "wrong password")

        return self.__token.create_tokens(user.id)


def get_user_repo(
        session:        AsyncSession = Depends(get_session),
        haser:          Hasher = Depends(get_hasher),
        token_logic:    TokenLogic = Depends(get_token_logic),
    ) -> UserService:
    
    return UserService(session, haser, token_logic)
