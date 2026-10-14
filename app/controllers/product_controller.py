from dataclasses import asdict

from flask import Blueprint, jsonify, request

from app.services.product_service import create_product, list_products


product_controller = Blueprint("products", __name__)


@product_controller.get("/api/products")
def get_products():
    return jsonify([asdict(product) for product in list_products()])


@product_controller.post("/api/products")
def post_product():
    data = request.get_json()
    if data["price"] < 0:
        return jsonify({"error": "price must be non-negative"}), 400

    product = create_product(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        stock=data["stock"],
    )
    return jsonify(asdict(product)), 201
