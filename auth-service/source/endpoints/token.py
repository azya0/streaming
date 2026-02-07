from fastapi import APIRouter, Depends

from service.token import ITokenService, get_token_service
from kernel.tokens import Tokens

router = APIRouter(
    prefix="/token",
    tags=["token"]
)


@router.get("/refresh", response_model=Tokens)
async def refresh(access_token: str, token_service: ITokenService = Depends(get_token_service)):
    return await token_service.refresh(access_token)
