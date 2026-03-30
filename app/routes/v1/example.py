from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import limiter
from app.utils.sanitizer import sanitize_dict
from app.modules.example.controller import ExampleController

example_bp = Blueprint("example", __name__, url_prefix="/example")


@example_bp.route("", methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def list_examples():
    return jsonify(ExampleController().list()), 200


@example_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def get_example(user_id):
    return jsonify(ExampleController().get(user_id)), 200


@example_bp.route("", methods=["POST"])
@jwt_required()
@limiter.limit("10 per minute")
def create_example():
    return jsonify(ExampleController().create(sanitize_dict(request.json or {}))), 201


@example_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@limiter.limit("10 per minute")
def delete_example(user_id):
    ExampleController().delete(user_id)
    return jsonify({"message": "Deleted successfully"}), 200
