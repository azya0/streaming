from datetime import datetime

from fastapi import Depends

from database.engine import get_session, AsyncSession
from database.models import User as UserORM
from database.queries.user import (
    create_user, CreateStatus,
    get_user,
    delete_user, DeleteStatus,
    get_user_by_username,
    user_from_token
)
from kernel.hashing import get_hasher, Hasher
from kernel.tokens import get_token_logic, TokenLogic
from scheme.tokens import TokenScheme

from ..interfaces.user import IUserService, UserCreate, UserResult, UserAuth, Tokens
from ..exceptions import UnexpectedError
from .exceptions import (
    CreateUsernameTaken, UserNotFound, 
    WrongPassword, WrongTokenData,
    TokenNotActual, PermissionDenied
)


class UserService(IUserService):
    def __init__(self, session: AsyncSession, hasher: Hasher, token_logic: TokenLogic):
        assert isinstance(session, AsyncSession)

        self.__session: AsyncSession = session
        self.__hasher:  Hasher = hasher
        self.__token:   TokenLogic = token_logic
    
    async def __get_user_from_token(self, token: TokenScheme) -> UserORM:
        user_result = await user_from_token(
            self.__session,
            id=token.id,
            creation_data=datetime.fromtimestamp(token.created),
        )

        if (error := user_result.error()) is not None:
            raise TokenNotActual(error)
        
        return user_result.result()
    
    async def create(self, user_data: UserCreate) -> UserResult:
        password_hash = await self.__hasher.hash(user_data.password)
        
        result = await create_user(
            self.__session,
            user_data.username,
            password_hash
        )

        if (error := result.error()) is None:
            return UserResult.model_validate(result.result())

        if error is CreateStatus.AlreadyExists:
            raise CreateUsernameTaken()
        
        raise UnexpectedError()
    
    async def get(self, id: int) -> UserResult:
        user = await get_user(self.__session, id, actual=True)

        if user is None:
            raise UserNotFound()
        
        return UserResult.model_validate(user)

    async def delete(self, access_token: str, id: int) -> None:
        validate_status = self.__token.validate(access_token)

        if (error := validate_status.error()) is not None:
            raise WrongTokenData(error)
        
        token_scheme = validate_status.result()
        
        user = await self.__get_user_from_token(token_scheme)

        if user.id != id and not user.is_admin:
            raise PermissionDenied()

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
