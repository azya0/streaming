from ..interfaces.exceptions import IServiceError


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
