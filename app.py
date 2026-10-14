import sqlite3

from flask import Flask, g, jsonify, request


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(DATABASE="products.db")
    if test_config is not None:
        app.config.update(test_config)

    database = app.config["DATABASE"]
    if database == ":memory:":
        database = f"file:products_{id(app)}?mode=memory&cache=shared"
        app.extensions["database_anchor"] = sqlite3.connect(database, uri=True)
    app.config["DATABASE_URI"] = database

    def connect_db():
        database_uri = app.config["DATABASE_URI"]
        connection = sqlite3.connect(
            database_uri,
            uri=database_uri.startswith("file:"),
        )
        connection.row_factory = sqlite3.Row
        return connection

    if "database_anchor" in app.extensions:
        schema_connection = app.extensions["database_anchor"]
    else:
        schema_connection = connect_db()
    schema_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )
    schema_connection.commit()
    if "database_anchor" not in app.extensions:
        schema_connection.close()

    @app.teardown_appcontext
    def close_db(_error=None):
        connection = g.pop("database", None)
        if connection is not None:
            connection.close()

    def get_db():
        if "database" not in g:
            g.database = connect_db()
        return g.database

    @app.post("/api/products")
    def create_product():
        product = request.get_json(silent=True)
        if not isinstance(product, dict) or not {"name", "price"} <= product.keys():
            return jsonify({"error": "name and price are required"}), 400

        cursor = get_db().execute(
            "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
            (
                product["name"],
                product.get("description", ""),
                product["price"],
            ),
        )
        get_db().commit()
        return (
            jsonify(
                {
                    "id": cursor.lastrowid,
                    "name": product["name"],
                    "description": product.get("description", ""),
                    "price": product["price"],
                }
            ),
            201,
        )

    @app.get("/api/products")
    def list_products():
        products = get_db().execute(
            "SELECT id, name, description, price FROM products ORDER BY id"
        ).fetchall()
        return jsonify([dict(product) for product in products])

    return app
