from fastapi import Depends

from kernel.tokens import TokenLogic, Tokens, get_token_logic

from ..exceptions import UnexpectedError
from .exceptions import ValidationError, WrongType, TokenExpired
from ..interfaces.token import ITokenService


class TokenService(ITokenService):
    def __init__(self, token_logic: TokenLogic):
        self.__token_logic: TokenLogic   = token_logic

    async def refresh(self, access_token: str) -> Tokens:
        result = self.__token_logic.refresh_tokens(access_token)

        print(result)

        if (error := result.error()) is None:
            return result.result()
        
        match(error):
            case TokenLogic.RefreshStatus.DecodeError | TokenLogic.RefreshStatus.NotValidToken:
                raise ValidationError()
            case TokenLogic.RefreshStatus.WrongTokenType:
                raise WrongType()
            case TokenLogic.RefreshStatus.TokenExpired:
                raise TokenExpired()

        raise UnexpectedError()


def get_token_service(token_logic: TokenLogic = Depends(get_token_logic)):
    return TokenService(token_logic)
