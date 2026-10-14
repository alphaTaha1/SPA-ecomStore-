from flask import Flask

from app.config import DEFAULT_DATABASE
from app.controllers.product_controller import product_controller
from app.utilities.database import close_db, initialize_database


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(DATABASE=str(DEFAULT_DATABASE))
    if test_config is not None:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)
    app.register_blueprint(product_controller)

    with app.app_context():
        initialize_database()

    return app
