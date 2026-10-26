from flask import Blueprint, jsonify, request

from services.order_service import OrderValidationError, create_order


order_blueprint = Blueprint("orders", __name__)


@order_blueprint.post("/api/orders")
def post_order():
    payload = request.get_json(silent=True)
    items = payload.get("items") if isinstance(payload, dict) else None
    try:
        order = create_order(items)
    except OrderValidationError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify(order), 201
