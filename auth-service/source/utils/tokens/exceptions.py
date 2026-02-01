class TokenLogicException(Exception):
    pass


class WrongTokenType(TokenLogicException):
    pass


class NotValidToken(TokenLogicException):
    pass


class TokenExpired(TokenLogicException):
    pass
