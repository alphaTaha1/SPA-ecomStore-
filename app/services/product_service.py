from app.models.product import Product
from app.utilities.database import get_db


def create_product(name: str, description: str, price: float, stock: int) -> Product:
    connection = get_db()
    cursor = connection.execute(
        "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
        (name, description, price, stock),
    )
    connection.commit()
    return Product(
        id=cursor.lastrowid,
        name=name,
        description=description,
        price=price,
        stock=stock,
    )


def list_products() -> list[Product]:
    rows = get_db().execute(
        "SELECT id, name, description, price, stock FROM products ORDER BY id"
    ).fetchall()
    return [Product(**dict(row)) for row in rows]
