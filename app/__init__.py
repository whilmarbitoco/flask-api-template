from flask import Flask, jsonify
from app.errors.handlers import NotFoundError, APIError, ValidationError



def create_app():
    app = Flask(__name__)

    @app.errorhandler(APIError)
    def handle_api_errors(error):
        return jsonify(error.to_json()), error.status_code

    @app.route("/test")
    def test():
        raise ValidationError(message="This resource was not found.")

    return app