from enum import Enum

from pydantic import BaseModel


class TokenType(Enum):
    access  = 0
    refresh = 1


class TokenCodeScheme(BaseModel):
    id:     int
    expire: int
    type:   TokenType
