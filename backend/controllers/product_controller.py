from flask import Blueprint, jsonify, request

from services.product_service import (
    ProductValidationError,
    create_product,
    list_products,
)


product_blueprint = Blueprint("products", __name__)


@product_blueprint.post("/api/products")
def post_product():
    try:
        product = create_product(request.get_json(silent=True))
    except ProductValidationError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify(product), 201


@product_blueprint.get("/api/products")
def get_products():
    return jsonify(list_products())
