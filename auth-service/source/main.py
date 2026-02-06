from fastapi import FastAPI
import uvicorn

from settings import Settings
from endpoints import routers


def get_application() -> FastAPI:
    application = FastAPI(title="User microservice")

    for router in routers:
        application.include_router(router)

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
