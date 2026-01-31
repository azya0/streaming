from database.models import User as UserORM
from database.queries.user import create_user, CreateStatus

from utils.hashing import Hasher

from .interfaces.user import IUserRepository, UserCreate, UserResult


class UserRepositoryError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message

        super().__init__(message)


class UserRepository(IUserRepository):
    __hasher: Hasher = Hasher()
    
    @staticmethod
    async def create(user_data: UserCreate) -> UserResult:
        password_hash = await UserRepository.__hasher.hash(user_data.password)
        
        user = UserORM(
            username=user_data.username,
            password_hash=password_hash,
        )
        
        status: CreateStatus = await create_user(user)

        if status == CreateStatus.Ok:
            return UserResult.model_validate(user)
        
        message = "unexcpected"

        match(status):
            case CreateStatus.AlreadyExists:
                message = "username is already taken"
        
        raise UserRepositoryError(400, message)
