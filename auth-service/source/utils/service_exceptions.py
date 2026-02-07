from typing import Any

from fastapi import HTTPException, Request

from service.exceptions import IServiceError, UnexpectedError, service_exception_to_status_code


class ServiceExceptionsHandlerError(Exception):
    def __init__(self, type: Any):
        super().__init__(f"service_exception_to_status_code does not include: {type}")


def convert_error(error: IServiceError) -> HTTPException:
    if isinstance(error, UnexpectedError):
        return HTTPException(
            status_code=500,
            detail=str(error)            
        )

    _dict = service_exception_to_status_code.get(error.base_class())

    if _dict is None:
        raise ServiceExceptionsHandlerError(error)
    
    status_code: int = _dict.get(error.__class__)

    if status_code is None:
        raise ServiceExceptionsHandlerError(error)

    return HTTPException(
        status_code=status_code,
        detail=str(error)
    )


def service_exception_handler(request: Request, exc: Exception):
    raise convert_error(exc)
