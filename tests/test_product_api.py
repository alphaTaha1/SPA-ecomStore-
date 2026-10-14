from app.main import create_app


def test_lists_no_products_when_store_is_empty(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "products.db")})
    client = app.test_client()

    response = client.get("/api/products")

    assert response.status_code == 200
    assert response.get_json() == []


def test_creates_product_and_returns_created_product(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "products.db")})
    client = app.test_client()

    response = client.post(
        "/api/products",
        json={
            "name": "Widget",
            "description": "A test widget",
            "price": 12.5,
            "stock": 4,
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Widget",
        "description": "A test widget",
        "price": 12.5,
        "stock": 4,
    }


def test_rejects_product_with_negative_price(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "products.db")})
    app.config["PROPAGATE_EXCEPTIONS"] = False
    client = app.test_client()

    response = client.post(
        "/api/products",
        json={
            "name": "Widget",
            "description": "A test widget",
            "price": -1,
            "stock": 4,
        },
    )

    assert response.status_code == 400
