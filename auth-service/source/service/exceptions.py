from .interfaces.exceptions import IServiceError
from .user_service.exceptions import *


service_exception_to_status_code: dict[type[IServiceError], dict[type[IServiceError], int]] = {
    UserServiceException: {
        CreateUsernameTaken: 400,
        WrongPassword: 400,
        UserNotFound: 404,
    },
}
