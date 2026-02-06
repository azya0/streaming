from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from fastapi import HTTPException

from service.exceptions import IServiceError, service_exception_to_status_code

P = ParamSpec("P")
R = TypeVar("R")


class ServiceExceptionsHandlerError(Exception):
    def __init__(self, ):
        super().__init__()


def convert_error(error: IServiceError) -> HTTPException:
    _dict = service_exception_to_status_code.get(error.base_class())

    if _dict is None:
        raise ServiceExceptionsHandlerError()
    
    status_code: int = _dict.get(error.__class__)

    if status_code is None:
        raise ServiceExceptionsHandlerError()

    return HTTPException(
        status_code=status_code,
        detail=str(error)
    )


def service_exception_handler(old_function: Callable[P, R]) -> Callable[P, R]:
    @wraps(old_function)
    async def new_function(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            result = await old_function(*args, **kwargs)
        except IServiceError as error:
            raise convert_error(error)

        return result
    return new_function
