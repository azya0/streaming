from typing_extensions import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from settings import DatabaseConfig

settings = DatabaseConfig()

engine = create_async_engine(
    url=settings.get_postgres_build(),
    echo=False,
)

session_factory = async_sessionmaker(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_factory()

    async with session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as exception:
            await session.rollback()
            raise exception
        finally:
            await session.close()
