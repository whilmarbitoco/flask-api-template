import os
from flask import Flask, jsonify
from app.errors.handlers import APIError
from app.core.logging import configure_logging
from app.api.v1.users.route import users_bp
from app.core.config import config_map
from .extensions import db, migrate


env = os.getenv("FLASK_ENV", "development")

def create_app():
    app = Flask(__name__)

    @app.errorhandler(APIError)
    def handle_api_errors(error):
        return jsonify(error.to_json()), error.status_code

    # Registered middleware, extensions
    app.config.from_object(config_map[env])
    configure_logging()
    db.init_app(app)
    migrate.init_app(app, db)
    from app.modules.users import model

    # Register blueprints
    app.register_blueprint(users_bp)

    return app