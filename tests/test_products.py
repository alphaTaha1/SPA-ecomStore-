from fastapi.testclient import TestClient
from sqlalchemy import select

from app.database import Database, create_database
from app.main import create_app
from app.models import Base, Product
from app.seed import DEFAULT_PRODUCTS, seed_products


def test_database_creates_products_table_with_default_stock(tmp_path):
    database = Database(f"sqlite:///{tmp_path / 'products.db'}")

    try:
        Base.metadata.create_all(bind=database.engine)
        with database.session_factory() as session:
            product = Product(name="Notebook", price=4.5)
            session.add(product)
            session.commit()
            session.refresh(product)

            assert product.id is not None
            assert product.stock == 10
            assert product.category is None
    finally:
        database.dispose()


def test_app_seeds_default_products_once(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'seeded-products.db'}"

    for _ in range(2):
        with TestClient(create_app(database_url)):
            engine, session_factory = create_database(database_url)
            try:
                with session_factory() as session:
                    products = list(
                        session.scalars(select(Product).order_by(Product.id))
                    )

                assert len(products) == len(DEFAULT_PRODUCTS)
                assert products[0].name == "Wireless Mouse"
                assert products[0].price == 24.99
                assert products[0].stock == 35
            finally:
                engine.dispose()


def test_seed_products_preserves_existing_product(tmp_path):
    database = Database(f"sqlite:///{tmp_path / 'existing-product.db'}")

    try:
        Base.metadata.create_all(bind=database.engine)
        with database.session_factory.begin() as session:
            session.add(Product(name="Custom Product", price=9.99, stock=3))

        seed_products(database.session_factory)

        with database.session_factory() as session:
            products = list(session.scalars(select(Product)))

        assert len(products) == 1
        assert products[0].name == "Custom Product"
    finally:
        database.dispose()


def test_create_and_list_products(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'product-api.db'}")

    with TestClient(app) as client:
        root = client.get("/")
        assert root.status_code == 200
        assert root.json()["products"] == "/products"
        assert root.json()["docs"] == "/docs"

        created = client.post(
            "/products",
            json={
                "name": "Travel Mug",
                "price": 16.5,
                "category": "Accessories",
                "stock": 8,
            },
        )

        assert created.status_code == 201
        product = created.json()
        assert product == {
            "id": 6,
            "name": "Travel Mug",
            "price": 16.5,
            "category": "Accessories",
            "stock": 8,
        }

        listed = client.get("/products")
        assert listed.status_code == 200
        products = listed.json()
        assert len(products) == len(DEFAULT_PRODUCTS) + 1
        assert products[-1] == product


def test_create_product_uses_default_stock(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'product-default-stock.db'}")

    with TestClient(app) as client:
        created = client.post(
            "/products",
            json={"name": "Desk Lamp", "price": 29.95},
        )

        assert created.status_code == 201
        assert created.json()["stock"] == 10


def test_create_product_rejects_negative_price(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'invalid-product.db'}")

    with TestClient(app) as client:
        created = client.post(
            "/products",
            json={"name": "Invalid Product", "price": -1},
        )

        assert created.status_code == 422
    