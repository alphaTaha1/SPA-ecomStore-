import unittest

from app import create_app


class OrderPlacementTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "DATABASE": ":memory:"})
        self.client = self.app.test_client()
        self.client.post(
            "/api/products",
            json={"name": "Desk Lamp", "price": 29.99},
        )

    def test_placing_an_order_returns_its_items_and_calculated_total(self):
        response = self.client.post(
            "/api/orders",
            json={"items": [{"product_id": 1, "quantity": 2}]},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "id": 1,
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 2,
                        "unit_price": 29.99,
                        "subtotal": 59.98,
                    }
                ],
                "total": 59.98,
            },
        )

    def test_order_requires_a_non_empty_items_list(self):
        for order in ({}, {"items": []}, {"items": "invalid"}):
            with self.subTest(order=order):
                response = self.client.post("/api/orders", json=order)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "items must be a non-empty list"},
                )

    def test_order_rejects_unknown_products(self):
        response = self.client.post(
            "/api/orders",
            json={"items": [{"product_id": 999, "quantity": 1}]},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "product 999 does not exist"},
        )

    def test_order_requires_positive_integer_quantities(self):
        for quantity in (0, -1, 1.5, "2", True):
            with self.subTest(quantity=quantity):
                response = self.client.post(
                    "/api/orders",
                    json={"items": [{"product_id": 1, "quantity": quantity}]},
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "quantity must be a positive integer"},
                )

    def test_order_items_require_product_id_and_quantity(self):
        for item in ({}, {"product_id": 1}, {"quantity": 1}, None):
            with self.subTest(item=item):
                response = self.client.post(
                    "/api/orders",
                    json={"items": [item]},
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "each item must include product_id and quantity"},
                )

    def test_order_requires_positive_integer_product_ids(self):
        for product_id in (0, -1, 1.5, "1", True, None):
            with self.subTest(product_id=product_id):
                response = self.client.post(
                    "/api/orders",
                    json={
                        "items": [{"product_id": product_id, "quantity": 1}]
                    },
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "product_id must be a positive integer"},
                )

    def test_order_total_avoids_floating_point_artifacts(self):
        first_product = self.client.post(
            "/api/products",
            json={"name": "First", "price": 0.1},
        ).get_json()
        second_product = self.client.post(
            "/api/products",
            json={"name": "Second", "price": 0.2},
        ).get_json()

        response = self.client.post(
            "/api/orders",
            json={
                "items": [
                    {"product_id": first_product["id"], "quantity": 1},
                    {"product_id": second_product["id"], "quantity": 1},
                ]
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["total"], 0.3)


if __name__ == "__main__":
    unittest.main()
