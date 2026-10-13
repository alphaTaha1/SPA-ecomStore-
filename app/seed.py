from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.models import Product


DEFAULT_PRODUCTS: tuple[tuple[str, float, str, int], ...] = (
    ("Wireless Mouse", 24.99, "Electronics", 35),
    ("Mechanical Keyboard", 79.99, "Electronics", 18),
    ("USB-C Hub", 39.50, "Electronics", 22),
    ("Everyday Backpack", 54.00, "Accessories", 12),
    ("Insulated Water Bottle", 18.75, "Accessories", 40),
)


def seed_products(session_factory: sessionmaker[Session]) -> None:
    with session_factory.begin() as session:
        existing_product_id = session.scalar(select(Product.id).limit(1))
        if existing_product_id is not None:
            return

        session.add_all(
            Product(name=name, price=price, category=category, stock=stock)
            for name, price, category, stock in DEFAULT_PRODUCTS
        )
