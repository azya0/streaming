from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Callable

from fastapi import Depends
import jwt
from pydantic_core import ValidationError

from utils.expected import *
from settings import JwtTokensConfig, get_token_config
from scheme.tokens import TokenScheme, TokenType


@dataclass
class Tokens:
    ACCESS_TOKEN:   str
    REFRESH_TOKEN:  str


class TokenLogic:
    def __init__(self, settings: JwtTokensConfig):
        self.__settings:    JwtTokensConfig = settings
        
        self.__access_expire:  timedelta = timedelta(
            minutes=self.__settings.ACCESS_EXPIRES
        )
        self.__refresh_expire: timedelta = timedelta(
            days=self.__settings.REFRESH_EXPIRES
        )

    def __create_token(self, payload: TokenScheme) -> str:
        return jwt.encode(
            payload.model_dump(),
            self.__settings.SECRET_KEY,
            self.__settings.ALGORITHM,
        )
    
    def __get_timestamp(self, current_time: datetime, delta_time: timedelta) -> int:
        return int((current_time + delta_time).timestamp())
    
    def create_tokens(self, id: int) -> Tokens:
        current_time: datetime = datetime.now()
        
        create_by_data: Callable[[int, TokenType], TokenScheme] \
            = lambda expire, type : self.__create_token(TokenScheme(
                id=id,
                expire=expire,
                type=type.value,
                )
            )
        
        get_timestamp: Callable[[timedelta], int] \
            = lambda delta_time : self.__get_timestamp(current_time, delta_time)

        return Tokens(
            create_by_data(get_timestamp(self.__access_expire), TokenType.access),
            create_by_data(get_timestamp(self.__refresh_expire), TokenType.refresh),
        )
    
    class RefreshStatus(int, Enum):
        Ok = 0
        DecodeError = 1
        NotValidToken = 2
        WrongTokenType = 3
        TokenExpired = 4

    def refresh_tokens(self, access_token: str) -> Expected[Tokens, RefreshStatus]:
        current_time: datetime = datetime.now()

        try:
            payload = jwt.decode(
                access_token,
                self.__settings.SECRET_KEY,
                self.__settings.ALGORITHM
            )
        except jwt.exceptions.DecodeError:
            return Error(TokenLogic.RefreshStatus.DecodeError)

        try:
            scheme = TokenScheme.model_validate(payload)
        except ValidationError:
            return Error(TokenLogic.RefreshStatus.NotValidToken)

        if scheme.type != TokenType.access:
            return Error(TokenLogic.RefreshStatus.WrongTokenType)
        
        if int(current_time.timestamp()) > scheme.expire:
            return Error(TokenLogic.RefreshStatus.TokenExpired)
        
        tokens = self.create_tokens(scheme.id)

        return Ok(tokens)


@lru_cache
def get_token_logic(settings: JwtTokensConfig = Depends(get_token_config)):
    return TokenLogic(settings)
