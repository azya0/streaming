from ..interfaces.exceptions import IServiceError
from ..token.token import TokenLogic

from database.queries.user import TokenActualStatus 


class UserServiceException(IServiceError):
    @staticmethod
    def base_class() -> type[IServiceError]:
        return UserServiceException


class CreateUsernameTaken(UserServiceException):
    def __init__(self):
        super().__init__("username is already taken")


class UserNotFound(UserServiceException):
    def __init__(self):
        super().__init__("user not found")


class WrongPassword(UserServiceException):
    def __init__(self):
        super().__init__("wrong password")


class WrongTokenData(UserServiceException):
    ValidatationStatus = TokenLogic.ValidatationStatus

    def __get_message(self, status: ValidatationStatus) -> str:
        match(status):
            case self.ValidatationStatus.DecodeError:
                return "decode error"
            case self.ValidatationStatus.NotValidToken:
                return "wrong token structure"
            case self.ValidatationStatus.WrongTokenType:
                return "wrong token type (confused about access and refresh)"
            case self.ValidatationStatus.TokenExpired:
                return "token expired"

        return "unexpected error"

    def __init__(self, status: ValidatationStatus):
        message: str = self.__get_message(status)

        super().__init__(f"refresh token exception: {message}")


class TokenNotActual(UserServiceException):
    @staticmethod
    def __get_message(status: TokenActualStatus) -> str:
        match(status):
            case TokenActualStatus.NotFound:
                return "user wasn't found in database"
            case TokenActualStatus.NotActive:
                return "user is not active (deleted)"
            case TokenActualStatus.TimeExpired:
                return "user was changed after this token creation"
        
        return "unexpected error"
   
    def __init__(self, status: TokenActualStatus):
        message: str = self.__get_message(status)

        super().__init__(f"refresh token exception: {message}")


class PermissionDenied(UserServiceException):
    def __init__(self):
        super().__init__("permission denied")
