from flask import Flask

from controllers.product_controller import product_blueprint
from utility.database import init_app as init_database


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(DATABASE="products.db")
    if test_config is not None:
        app.config.update(test_config)

    init_database(app)
    app.register_blueprint(product_blueprint)
    return app
