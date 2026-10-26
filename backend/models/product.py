import sqlite3


def initialize(connection):
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )
    connection.commit()


def create(connection, name, description, price):
    cursor = connection.execute(
        "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
        (name, description, price),
    )
    connection.commit()
    product = connection.execute(
        "SELECT id, name, description, price FROM products WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()
    return dict(product)


def list_all(connection):
    products = connection.execute(
        "SELECT id, name, description, price FROM products ORDER BY id"
    ).fetchall()
    return [dict(product) for product in products]
