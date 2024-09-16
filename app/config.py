from dotenv import load_dotenv
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings


load_dotenv()


class PGConfig(BaseSettings):
    postgres_host: str | None = "localhost"
    postgres_port: int = 5432
    postgres_database: str = ""
    postgres_username: str | None = None
    postgres_password: str | None = None
    scheme: str = "postgresql+asyncpg"
    echo: bool = False

    @property
    def pg_dsn(self):
        pg_dsn: str = PostgresDsn.build(
            scheme=self.scheme,
            host=self.postgres_host,
            port=self.postgres_port,
            username=self.postgres_username,
            password=self.postgres_password,
            path=self.postgres_database
        ).unicode_string()
        return pg_dsn
