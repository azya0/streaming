from ..interfaces.exceptions import IServiceError


class TokenServiceException(IServiceError):
    @staticmethod
    def base_class() -> type[IServiceError]:
        return TokenServiceException


class ValidationError(TokenServiceException):
    def __init__(self):
        super().__init__("this access token is not valid")


class WrongType(TokenServiceException):
    def __init__(self):
        super().__init__("this is not an access token")


class TokenExpired(TokenServiceException):
    def __init__(self):
        super().__init__("access token is expired")
