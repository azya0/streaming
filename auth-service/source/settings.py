from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


# Setting for database engine
class DatabaseConfig(BaseSettings):
    HOST:       str = Field(alias="AUTH_DB_HOST")
    PORT:       int = Field(alias="AUTH_DB_PORT")

    NAME:       str = Field(alias="AUTH_DB_NAME")

    SECRET_KEY: str = Field(alias="AUTH_DB_SECRET_KEY")

    USER:       str = Field(alias="AUTH_DB_USER")
    PASSWORD:   str = Field(alias="AUTH_DB_PASSWORD")

    SCHEME:     str = Field(
        default="postgresql+asyncpg",
        alias="AUTH_DB_SCHEME"
    )

    def to_dict(self) -> dict[str, str | int]:
        # dict for PostgreDsn build

        return {
            "scheme":   self.SCHEME,
            "username": self.USER,
            "password": self.PASSWORD,
            "host":     self.HOST,
            "port":     self.PORT,
            "path":     self.NAME,
        }

    def get_postgres_build(self) -> PostgresDsn:
        return PostgresDsn.build(**self.to_dict())


# Global setting for binding api
class Settings(BaseSettings):
    HOST: str
    PORT: int
