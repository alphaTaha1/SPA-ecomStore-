from models import product as product_model
from utility.database import get_db


class ProductValidationError(ValueError):
    pass


def create_product(product):
    if not isinstance(product, dict) or not {"name", "price"} <= product.keys():
        raise ProductValidationError("name and price are required")

    return product_model.create(
        get_db(),
        product["name"],
        product.get("description", ""),
        product["price"],
    )


def list_products():
    return product_model.list_all(get_db())
