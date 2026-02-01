from fastapi import APIRouter, Depends

from repository import get_user_repo, IUserRepository
from scheme.request import User as UserRequest, UserAuth as UserRequestAuth
from scheme.response import User as UserResponse, Tokens
from utils.exceptions import repository_exception_handler


router = APIRouter(
    prefix="/auth",
)


@router.post("/registration", response_model=UserResponse)
@repository_exception_handler
async def register_user(user: UserRequest, repository: IUserRepository = Depends(get_user_repo)):
    return await repository.create(user)


@router.get("/get/{id}", response_model=UserResponse)
@repository_exception_handler
async def get_user(id: int, repository: IUserRepository = Depends(get_user_repo)):
    return await repository.get(id)


@router.delete("/delete/{id}", status_code=200)
@repository_exception_handler
async def delete_user(id: int, repository: IUserRepository = Depends(get_user_repo)):
    return await repository.delete(id)


@router.post("/login", response_model=Tokens)
@repository_exception_handler
async def login(user: UserRequestAuth, repository: IUserRepository = Depends(get_user_repo)):
    return await repository.login(user)
