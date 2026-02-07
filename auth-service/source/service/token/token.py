from fastapi import Depends

from kernel.tokens import TokenLogic, Tokens, get_token_logic

from ..interfaces.token import ITokenService


class TokenService(ITokenService):
    def __init__(self, token_logic: TokenLogic):
        self.__token_logic: TokenLogic   = token_logic

    async def refresh(self, access_token: str) -> Tokens:
        self.__token_logic.refresh_tokens(access_token)


def get_token_service(token_logic: TokenLogic = Depends(get_token_logic)):
    return TokenService(token_logic)
