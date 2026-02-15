from enum import Enum

from pydantic import BaseModel


class TokenType(int, Enum):
    access  = 0
    refresh = 1


class TokenCodeScheme(BaseModel):
    id:         int
    created:    int
    expire:     int
    type:       TokenType
