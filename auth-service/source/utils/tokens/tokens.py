from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Callable

from jwt import JWT
from pydantic_core import ValidationError

from settings import JwtTokensConfig
from scheme.tokens import TokenScheme, TokenType

from .exceptions import TokenExpired, WrongTokenType, NotValidToken


@dataclass
class Tokens:
    ACCESS_TOKEN:   str
    REFRESH_TOKEN:  str


class TokenLogic:
    def __init__(self, settings: JwtTokensConfig, jwt: JWT):
        self.__settings:    JwtTokensConfig = settings
        self.__jwt:         JWT = jwt
        
        self.__access_expire:  timedelta = timedelta(
            min=self.__settings.ACCESS_EXPIRES
        )
        self.__refresh_expire: timedelta = timedelta(
            days=self.__settings.REFRESH_EXPIRES
        )

    def __create_token(self, payload: TokenScheme) -> str:
        return self.__jwt.encode(
            payload.model_dump(),
            self.__settings.SECRET_KEY,
            self.__settings.ALGORITHM,
        )
    
    def __get_timestamp(current_time: datetime, delta_time: timedelta) -> int:
        return int((current_time + delta_time).timestamp())
    
    def create_tokens(self, id: int) -> Tokens:
        current_time: datetime = datetime.now()
        
        create_by_data: Callable[[int, str], TokenScheme] \
            = lambda expire, type : self.__create_token(TokenScheme(
                id=id,
                expire=expire,
                type=type,
                )
            )
        
        get_timestamp: Callable[[timedelta], int] \
            = lambda delta_time : self.__get_timestamp(current_time, delta_time)

        return Tokens(
            create_by_data(get_timestamp(self.__access_expire), TokenType.access),
            create_by_data(get_timestamp(self.__refresh_expire), TokenType.refresh),
        )

    def refresh_tokens(self, access_token: str) -> Tokens:
        current_time: datetime = datetime.now()

        payload = self.__jwt.decode(access_token, self.__settings.SECRET_KEY)

        try:
            scheme = TokenScheme.model_validate(payload)
        except ValidationError:
            raise NotValidToken

        if scheme.type != TokenType.access:
            raise WrongTokenType
        
        if int(current_time.timestamp()) > scheme.expire:
            raise TokenExpired
        
        return self.create_tokens(scheme.id)
