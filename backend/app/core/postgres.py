from sqlmodel import Session, create_engine

from app.settings import PostgresSettings

settings = PostgresSettings()

DATABASE_URL = (
    f"postgresql://"
    f"{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_uri}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)

engine = create_engine(DATABASE_URL)


def get_db_session() -> Session:
    with Session(engine) as session:
        yield session
