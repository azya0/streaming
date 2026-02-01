from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from fastapi import HTTPException

from repository.exceptions import RepositoryError

P = ParamSpec("P")
R = TypeVar("R")


def repository_exception_handler(old_function: Callable[P, R]) -> Callable[P, R]:
    @wraps(old_function)
    async def new_function(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            result = await old_function(*args, **kwargs)
        except RepositoryError as error:
            raise HTTPException(
                status_code=error.status,
                detail=error.message
            )
        
        return result
    return new_function
