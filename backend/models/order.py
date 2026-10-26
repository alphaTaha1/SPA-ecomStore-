from decimal import Decimal


def initialize(connection):
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL REFERENCES orders(id),
            product_id INTEGER NOT NULL REFERENCES products(id),
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL
        )
        """
    )
    connection.commit()


def create(connection, items):
    calculated_items = [
        {
            **item,
            "subtotal": Decimal(str(item["unit_price"])) * item["quantity"],
        }
        for item in items
    ]
    total = sum(
        (item["subtotal"] for item in calculated_items),
        start=Decimal("0"),
    )
    cursor = connection.execute(
        "INSERT INTO orders (total) VALUES (?)",
        (float(total),),
    )
    order_id = cursor.lastrowid
    connection.executemany(
        """
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
        """,
        [
            (order_id, item["product_id"], item["quantity"], item["unit_price"])
            for item in items
        ],
    )
    connection.commit()
    return {
        "id": order_id,
        "items": [
            {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "unit_price": item["unit_price"],
                "subtotal": float(item["subtotal"]),
            }
            for item in calculated_items
        ],
        "total": float(total),
    }
