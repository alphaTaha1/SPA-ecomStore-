
import os
from collections.abc import Generator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_database(database_url: str | None = None):
    load_dotenv(Path.cwd() / ".env")

    url = database_url or os.getenv(
        "DATABASE_URL", "sqlite:///./app.db"
    )

    connect_args = (
        {"check_same_thread": False}
        if url.startswith("sqlite")
        else {}
    )

    engine = create_engine(url, connect_args=connect_args)

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    return engine, session_factory


class Database:
    def __init__(self, database_url: str | None = None):
        self.engine, self.session_factory = create_database(
            database_url
        )

    def get_session(self) -> Generator[Session, None, None]:
        yield from get_session(self.session_factory)

    def dispose(self) -> None:
        self.engine.dispose()


def get_session(
    session_factory: sessionmaker,
) -> Generator[Session, None, None]:
    with session_factory() as session:
        yield session
