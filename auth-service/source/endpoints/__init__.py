from fastapi import APIRouter

from .auth import router as auth_router

routers: tuple[APIRouter] = (
    auth_router,
)
