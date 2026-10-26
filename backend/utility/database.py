import sqlite3
import uuid

from flask import current_app, g

from models.order import initialize as initialize_order_tables
from models.product import initialize as initialize_product_table


def _connect(database_uri):
    connection = sqlite3.connect(
        database_uri,
        uri=database_uri.startswith("file:"),
    )
    connection.row_factory = sqlite3.Row
    return connection


def get_db():
    if "database" not in g:
        g.database = _connect(current_app.config["DATABASE_URI"])
    return g.database


def close_db(_error=None):
    connection = g.pop("database", None)
    if connection is not None:
        connection.close()


def init_app(app):
    database_uri = app.config["DATABASE"]
    if database_uri == ":memory:":
        database_uri = f"file:products_{uuid.uuid4()}?mode=memory&cache=shared"
        app.extensions["database_anchor"] = sqlite3.connect(database_uri, uri=True)
    app.config["DATABASE_URI"] = database_uri

    if "database_anchor" in app.extensions:
        schema_connection = app.extensions["database_anchor"]
    else:
        schema_connection = _connect(database_uri)
    initialize_product_table(schema_connection)
    initialize_order_tables(schema_connection)
    if "database_anchor" not in app.extensions:
        schema_connection.close()

    app.teardown_appcontext(close_db)
