from fastapi import APIRouter, Depends

from service import get_user_repo, IUserService
from scheme.request import User as UserRequest, UserAuth as UserRequestAuth
from scheme.response import User as UserResponse, Tokens
from scheme.oauth2 import oauth2_scheme


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/registration", response_model=UserResponse)
async def register_user(user: UserRequest, service: IUserService = Depends(get_user_repo)):
    return await service.create(user)


@router.get("/get/{id}", response_model=UserResponse)
async def get_user(id: int, service: IUserService = Depends(get_user_repo)):
    return await service.get(id)


@router.delete("/delete/{id}", status_code=200)
async def delete_user(
    id: int,
    token: str = Depends(oauth2_scheme),
    service: IUserService = Depends(get_user_repo)
):
    return await service.delete(token, id)


@router.post("/login", response_model=Tokens)
async def login(user: UserRequestAuth, service: IUserService = Depends(get_user_repo)):
    return await service.login(user)
