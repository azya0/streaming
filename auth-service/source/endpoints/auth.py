from fastapi import APIRouter, Depends

from service import get_user_repo, IUserService
from scheme.request import User as UserRequest, UserAuth as UserRequestAuth
from scheme.response import User as UserResponse, Tokens
from utils.service_exceptions import service_exception_handler


router = APIRouter(
    prefix="/auth",
)


@router.post("/registration", response_model=UserResponse)
@service_exception_handler
async def register_user(user: UserRequest, service: IUserService = Depends(get_user_repo)):
    return await service.create(user)


@router.get("/get/{id}", response_model=UserResponse)
@service_exception_handler
async def get_user(id: int, service: IUserService = Depends(get_user_repo)):
    return await service.get(id)


@router.delete("/delete/{id}", status_code=200)
@service_exception_handler
async def delete_user(id: int, service: IUserService = Depends(get_user_repo)):
    return await service.delete(id)


@router.post("/login", response_model=Tokens)
@service_exception_handler
async def login(user: UserRequestAuth, service: IUserService = Depends(get_user_repo)):
    return await service.login(user)
