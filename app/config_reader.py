from pydantic import BaseSettings, BaseModel, PostgresDsn


class PostgresConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str | None = None
    database: str = "postgres"

    echo: bool = False

    @property
    def dsn(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.user,
            password=self.password,
            host=self.host,
            port=f"{self.port}",
            path=f"/{self.database}",
        )


class Config(BaseSettings):
    postgres: PostgresConfig

    class Config:
        frozen = True

        env_file = ".env"
        env_nested_delimiter = "__"
        env_file_encoding = "utf-8"


config = Config()
