from fastapi import Depends

from database.engine import get_session, AsyncSession
from database.models import User as UserORM
from database.queries.user import (
    create_user,
    get_user,
    delete_user, DeleteStatus,
    get_user_by_username,
)
from kernel.hashing import get_hasher, Hasher
from kernel.tokens import get_token_logic, TokenLogic

from ..interfaces.user import IUserService, UserCreate, UserResult, UserAuth, Tokens
from .exceptions import *


class UserService(IUserService):
    def __init__(self, session: AsyncSession, hasher: Hasher, token_logic: TokenLogic):
        assert isinstance(session, AsyncSession)

        self.__session: AsyncSession = session
        self.__hasher:  Hasher = hasher
        self.__token:   TokenLogic = token_logic
    
    async def create(self, user_data: UserCreate) -> UserResult:
        password_hash = await self.__hasher.hash(user_data.password)
        
        result = await create_user(
            self.__session,
            user_data.username,
            password_hash
        )

        if result.error() is None:
            return UserResult.model_validate(result.result())

        raise CreateUsernameTaken()
    
    async def get(self, id: int) -> UserResult:
        user = await get_user(self.__session, id, actual=True)

        if user is None:
            raise UserNotFound()
        
        return UserResult.model_validate(user)

    async def delete(self, id: int) -> None:
        status = await delete_user(self.__session, id)

        if status == DeleteStatus.Ok:
            return
        
        raise UserNotFound()
    
    async def login(self, user_data: UserAuth) -> Tokens:
        user: UserORM | None = await get_user_by_username(self.__session, user_data.username)

        if user is None:
            raise UserNotFound()

        if not await self.__hasher.verify(user.password_hash, user_data.password):
            raise WrongPassword()

        return self.__token.create_tokens(user.id)


def get_user_repo(
        session:        AsyncSession = Depends(get_session),
        haser:          Hasher = Depends(get_hasher),
        token_logic:    TokenLogic = Depends(get_token_logic),
    ) -> UserService:
    
    return UserService(session, haser, token_logic)
