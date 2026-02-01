from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


# Setting for database engine
class DatabaseConfig(BaseSettings):
    HOST:       str = Field(alias="AUTH_DB_HOST")
    PORT:       int = Field(alias="AUTH_DB_PORT")

    NAME:       str = Field(alias="AUTH_DB_NAME")

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
    HOST: str = Field(alias="AUTH_API_HOST")
    PORT: int = Field(alias="AUTH_API_PORT")


# Default constants
class ProgramConstants(BaseSettings):
    HASH_WORKERS_NUM: int = Field(
        default=4,
    )


class JwtTokensConfig(BaseSettings):
    SECRET_KEY:         str = Field(alias="AUTH_API_TOKENS_SECRET_KEY")

    ALGORITHM:          str = Field(
        default="HS512",
        alias="AUTH_API_TOKENS_JWT_ALGOTITHM"
    )
    
    ACCESS_EXPIRES:     str = Field(alias="AUTH_API_TOKENS_JWT_ACCESS_TOKEN_EXPIRES_MINUTE")
    REFRESH_EXPIRES:    str = Field(alias="AUTH_API_TOKENS_JWT_REFRESH_TOKEN_EXPIRES_DAYS")
