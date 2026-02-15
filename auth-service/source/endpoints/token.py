from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from service.token import ITokenService, get_token_service
from service.user import IUserService, get_user_repo
from kernel.tokens import Tokens
from scheme.request.user import UserAuth
from scheme.response.tokens import AcessTokenWithType

router = APIRouter(
    prefix="/token",
    tags=["token"]
)


@router.post("", response_model=AcessTokenWithType)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: IUserService = Depends(get_user_repo)):
    """form_data is used to integrate endpoint to swagger"""
    
    auth_scheme = UserAuth(
        username=form_data.username,
        password=form_data.password
    )
    
    result = await user_service.login(auth_scheme)

    return AcessTokenWithType(access_token=result.ACCESS_TOKEN, token_type="bearer")


@router.get("/refresh", response_model=Tokens)
async def refresh(refresh_token: str, token_service: ITokenService = Depends(get_token_service)):
    return await token_service.refresh(refresh_token)
