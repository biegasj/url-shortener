from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: str
    allowed_origins: str


class PostgresSettings(BaseSettings):
    postgres_password: str
    postgres_user: str
    postgres_db: str
    postgres_port: int
    postgres_uri: str
