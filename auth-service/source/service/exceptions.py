from .interfaces.exceptions import IServiceError, UnexpectedError
from .user.exceptions import *
from .token.exceptions import *


service_exception_to_status_code: dict[type[IServiceError], dict[type[IServiceError], int]] = {
    UserServiceException: {
        CreateUsernameTaken: 400,
        WrongPassword: 400,
        UserNotFound: 404,
        WrongTokenData: 403,
        TokenNotActual: 403,
        PermissionDenied: 403,
    },
    TokenServiceException: {
        ValidationError: 400,
        WrongType: 400,
        TokenExpired: 400,
    }
}
