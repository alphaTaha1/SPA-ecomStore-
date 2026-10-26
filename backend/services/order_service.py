from models import order as order_model
from utility.database import get_db


class OrderValidationError(ValueError):
    pass


def create_order(items):
    if not isinstance(items, list) or not items:
        raise OrderValidationError("items must be a non-empty list")

    connection = get_db()
    priced_items = []
    for item in items:
        if not isinstance(item, dict) or not {"product_id", "quantity"} <= item.keys():
            raise OrderValidationError(
                "each item must include product_id and quantity"
            )

        product_id = item["product_id"]
        if (
            isinstance(product_id, bool)
            or not isinstance(product_id, int)
            or product_id <= 0
        ):
            raise OrderValidationError("product_id must be a positive integer")

        quantity = item["quantity"]
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise OrderValidationError("quantity must be a positive integer")

        product = connection.execute(
            "SELECT price FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        if product is None:
            raise OrderValidationError(f"product {product_id} does not exist")

        priced_items.append(
            {
                "product_id": product_id,
                "quantity": item["quantity"],
                "unit_price": product["price"],
            }
        )

    return order_model.create(connection, priced_items)
