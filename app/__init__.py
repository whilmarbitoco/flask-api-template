from flask import Flask, jsonify
from app.errors.handlers import APIError
from app.core.logging import configure_logging
from app.api.v1.users.route import users_bp



def create_app():
    app = Flask(__name__)

    @app.errorhandler(APIError)
    def handle_api_errors(error):
        return jsonify(error.to_json()), error.status_code

    # Registered middleware, extensions
    configure_logging()

    # Register blueprints
    app.register_blueprint(users_bp)

    return app