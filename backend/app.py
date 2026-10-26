import os

from flask import Flask, jsonify, request

from controllers.order_controller import order_blueprint
from controllers.product_controller import product_blueprint
from utility.database import init_app as init_database


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.environ.get("DATABASE_PATH", "products.db"),
        FRONTEND_ORIGIN=os.environ.get(
            "FRONTEND_ORIGIN",
            "http://localhost:3000",
        ),
    )
    if test_config is not None:
        app.config.update(test_config)

    init_database(app)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(order_blueprint)

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin")
        if origin == app.config["FRONTEND_ORIGIN"]:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.vary.add("Origin")
        return response

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app
