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
