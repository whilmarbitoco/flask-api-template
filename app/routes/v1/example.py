from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError as MarshmallowValidationError
from app.extensions import limiter
from app.utils.sanitizer import sanitize_dict
from app.modules.example.model import ExampleCreate, ExampleRead
from app.modules.example.service import ExampleService
from app.errors.handlers import ValidationError

example_bp = Blueprint("example", __name__, url_prefix="/example")

service = ExampleService()
read_schema = ExampleRead()
create_schema = ExampleCreate()


@example_bp.route("", methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def list_examples():
    return jsonify(read_schema.dump(service.get_all(), many=True)), 200


@example_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def get_example(user_id):
    return jsonify(read_schema.dump(service.get_by_id(user_id))), 200


@example_bp.route("", methods=["POST"])
@jwt_required()
@limiter.limit("10 per minute")
def create_example():
    try:
        data = create_schema.load(sanitize_dict(request.json or {}))
    except MarshmallowValidationError as e:
        raise ValidationError(message=e.messages)
    return jsonify(read_schema.dump(service.create(**data))), 201


@example_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@limiter.limit("10 per minute")
def delete_example(user_id):
    service.delete(user_id)
    return jsonify({"message": "Deleted successfully"}), 200
