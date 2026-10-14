import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"])
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def initialize_database() -> None:
    Path(current_app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    connection = get_db()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            price REAL NOT NULL CHECK (price >= 0),
            stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
        )
        """
    )
    connection.commit()
