from fastapi import APIRouter, HTTPException

from repository import UserRepository, UserRepositoryError
from scheme.request import User as UserRequest
from scheme.response import User as UserResponse


router = APIRouter(
    prefix="/auth",
)


@router.post("/registration", response_model=UserResponse)
async def register_user(user: UserRequest):
    try:
        result = await UserRepository.create(user)
    except UserRepositoryError as error:
        raise HTTPException(
            status_code=error.status,
            detail=error.message
        )

    return result
