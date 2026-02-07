from fastapi import FastAPI
import uvicorn

from utils.service_exceptions import IServiceError, service_exception_handler
from endpoints import routers
from settings import Settings


def get_application() -> FastAPI:
    application = FastAPI(title="User microservice")

    for router in routers:
        application.include_router(router)

    application.exception_handler(IServiceError)(service_exception_handler)

    return application


def main():
    settings = Settings()
    application = get_application()

    uvicorn.run(
        application,
        host=settings.HOST,
        port=settings.PORT
    )


if __name__ == "__main__":
    main()
