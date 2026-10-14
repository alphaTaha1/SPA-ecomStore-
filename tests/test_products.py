import tempfile
import unittest
from pathlib import Path

from app import create_app
from services.product_service import ProductValidationError, create_product


class ProductCreationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "DATABASE": ":memory:"})
        self.client = self.app.test_client()

    def test_product_service_rejects_missing_required_fields(self):
        with self.assertRaises(ProductValidationError):
            create_product({"price": 29.99})

    def test_creating_a_product_returns_the_created_product(self):
        response = self.client.post(
            "/api/products",
            json={"name": "Desk Lamp", "description": "Adjustable", "price": 29.99},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "id": 1,
                "name": "Desk Lamp",
                "description": "Adjustable",
                "price": 29.99,
            },
        )

    def test_listing_returns_products_created_by_api(self):
        self.client.post(
            "/api/products",
            json={"name": "Desk Lamp", "description": "Adjustable", "price": 29.99},
        )

        response = self.client.get("/api/products")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            [
                {
                    "id": 1,
                    "name": "Desk Lamp",
                    "description": "Adjustable",
                    "price": 29.99,
                }
            ],
        )

    def test_product_creation_rejects_missing_required_fields(self):
        for product in (
            {"price": 29.99},
            {"name": "Desk Lamp"},
        ):
            with self.subTest(product=product):
                response = self.client.post("/api/products", json=product)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "name and price are required"},
                )

    def test_products_persist_between_app_instances(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "products.db"
            first_app = create_app({"TESTING": True, "DATABASE": str(database)})
            first_response = first_app.test_client().post(
                "/api/products",
                json={"name": "Desk Lamp", "description": "Adjustable", "price": 29.99},
            )

            second_app = create_app({"TESTING": True, "DATABASE": str(database)})
            second_response = second_app.test_client().get("/api/products")

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(
            second_response.get_json(),
            [
                {
                    "id": 1,
                    "name": "Desk Lamp",
                    "description": "Adjustable",
                    "price": 29.99,
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
