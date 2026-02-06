from enum import Enum


class ExpectedError(Exception):
    pass


class ExpectedCreationError(ExpectedError):
    def __init__(self, cls: Expected):
        super().__init__(f"Can't create instance of {cls}.")


class ExpectedResultError(ExpectedError):
    def __init__(self):
        super().__init__("Expected have no result")


class Expected[ReturnType, StatusCodes: (int, Enum)]:
    __allowed: set[Expected] = set()

    @classmethod
    def _add_allowed(cls, subclass: Expected):
        assert cls is not subclass and issubclass(subclass, cls)

        cls.__allowed.add(subclass)

    def __new__(cls) -> Expected[ReturnType, StatusCodes]:
        if cls not in Expected.__allowed:
            raise ExpectedCreationError(cls)
        
        return super().__new__(cls)

    def __init__(self, result: ReturnType | None = None, status_code: StatusCodes | None = None, is_error: bool = True):
        assert not (result is None and status_code is None)

        self.__is_error:    bool = is_error
        self.__error:       StatusCodes | None = status_code
        self.__result:      ReturnType  | None = result
    
    def __str__(self):
        if self.__is_error:
            return f"Unexpected error: {self.__error}"
        return f"Result: {self.__result}"

    def error(self) -> StatusCodes | None:
        if not self.__is_error:
            return
        
        return self.__error
    
    def result(self) -> ReturnType:
        if self.__is_error:
            raise ExpectedResultError()

        return self.__result


class __ExpectedBaseNew[T, K](Expected[T, K]):
    def __new__(cls, *args, **kwargs) -> Expected[T, K]:
        Expected._add_allowed(cls)

        return super().__new__(cls)


class Ok[T, K](__ExpectedBaseNew[T, K]):
    def __init__(self, result: T, status_code: K | None = None):
        super().__init__(
            result=result,
            status_code=status_code,
            is_error=False
        )


class Error[T, K: (int, Enum)](__ExpectedBaseNew[T, K]):
    def __init__(self, status_code: K):
        super().__init__(status_code=status_code)
