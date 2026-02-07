from abc import ABC, abstractmethod


class IServiceError(ABC, Exception):
    @staticmethod
    @abstractmethod
    def base_class() -> type[IServiceError]:
        """
        Return is a service base exception type
        
        IServiceError -> <IServiceBaseException> -> service exceptions
        """
        pass


class UnexpectedError(IServiceError):
    def __init__(self):
        super().__init__("this service error is unexpected. please ask developers about this problem")

    def base_class() -> type[IServiceError]:
        return UnexpectedError
