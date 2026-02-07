from fastapi import APIRouter

from .auth import router as auth_router
from .token import router as token_router

routers: tuple[APIRouter] = (
    auth_router,
    token_router,
)
